"""
Módulo de Chatbot conversacional basado en Vertex AI
"""
import logging
from typing import Dict, List, Optional
from google.cloud import aiplatform
from config.gcp_config import GCPConfig, MLConfig
from config.constants import MODEL_PARAMS, EQUIPMENT_TYPES, COMMON_ISSUES

logger = logging.getLogger(__name__)


class ChatbotModel:
    """Chatbot especializado en mantenimiento técnico"""
    
    def __init__(self):
        """Inicializa el modelo de chatbot"""
        self.project_id = GCPConfig.PROJECT_ID
        self.location = GCPConfig.VERTEX_AI_LOCATION
        self.model_id = GCPConfig.CHATBOT_MODEL_ID
        self.conversation_history: List[Dict] = []
        self.context = self._build_system_context()
        logger.info("Chatbot modelo inicializado")
    
    def _build_system_context(self) -> str:
        """Construye el contexto del sistema para el chatbot"""
        equipment_list = ", ".join(EQUIPMENT_TYPES)
        issues_list = ", ".join(COMMON_ISSUES)
        
        system_context = f"""
Eres un asistente de IA especializado en mantenimiento técnico industrial.
Tu rol es asistir a técnicos especializados en mantenimiento de equipos.

Equipos que conoces: {equipment_list}
Problemas comunes: {issues_list}

Responsabilidades:
1. Diagnosticar problemas técnicos basándote en descripciones del técnico
2. Proporcionar soluciones de mantenimiento preventivo y correctivo
3. Recomendar mejores prácticas de mantenimiento
4. Aprender de cada interacción para mejorar diagnósticos futuros
5. Mantener un historial de problemas y soluciones

Siempre solicita:
- Tipo de equipo
- Síntomas observados
- Historial de mantenimiento
- Entorno de operación

Responde en español, de manera profesional y técnica.
        """
        return system_context
    
    def send_message(self, user_message: str, session_id: Optional[str] = None) -> Dict:
        """
        Envía un mensaje al chatbot y obtiene una respuesta
        
        Args:
            user_message: Mensaje del usuario
            session_id: ID de sesión para mantener contexto
            
        Returns:
            Diccionario con la respuesta y metadatos
        """
        try:
            # Agregar mensaje del usuario al historial
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Llamar a Vertex AI para obtener respuesta
            response = self._call_vertex_ai(user_message)
            
            # Agregar respuesta al historial
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            return {
                "success": True,
                "response": response,
                "session_id": session_id,
                "message_count": len(self.conversation_history)
            }
            
        except Exception as e:
            logger.error(f"Error en chatbot: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "response": "Disculpe, hubo un error al procesar su consulta."
            }
    
    def _call_vertex_ai(self, message: str) -> str:
        """
        Llama a Vertex AI API
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            Respuesta del modelo
        """
        try:
            # Inicializar Vertex AI
            aiplatform.init(project=self.project_id, location=self.location)
            
            # Crear el modelo
            model = aiplatform.TextGenerationModel.from_pretrained(self.model_id)
            
            # Preparar prompt con contexto
            full_prompt = f"{self.context}\n\nMensaje del técnico: {message}"
            
            # Generar respuesta
            response = model.predict(
                prompt=full_prompt,
                max_output_tokens=MODEL_PARAMS['MAX_TOKENS'],
                temperature=MODEL_PARAMS['TEMPERATURE'],
                top_p=MODEL_PARAMS['TOP_P'],
                top_k=MODEL_PARAMS['TOP_K']
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error llamando a Vertex AI: {str(e)}")
            raise
    
    def get_conversation_history(self) -> List[Dict]:
        """Obtiene el historial de conversación"""
        return self.conversation_history
    
    def clear_history(self):
        """Limpia el historial de conversación"""
        self.conversation_history = []
        logger.info("Historial de conversación limpiado")
    
    def get_diagnostic_summary(self) -> Dict:
        """
        Genera un resumen del diagnóstico basado en la conversación
        
        Returns:
            Diccionario con resumen del diagnóstico
        """
        if not self.conversation_history:
            return {"summary": "No hay historial de conversación", "insights": []}
        
        try:
            # Usar Vertex AI para generar resumen
            aiplatform.init(project=self.project_id, location=self.location)
            model = aiplatform.TextGenerationModel.from_pretrained(self.model_id)
            
            # Convertir historial a texto
            conversation_text = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in self.conversation_history
            ])
            
            summary_prompt = f"""
Based on this maintenance conversation:
{conversation_text}

Provide a JSON summary with:
- diagnosed_problem
- severity (1-4)
- recommended_actions
- preventive_measures
- urgency
            """
            
            response = model.predict(
                prompt=summary_prompt,
                max_output_tokens=1024,
                temperature=0.3
            )
            
            return {
                "summary": response.text,
                "conversation_length": len(self.conversation_history)
            }
            
        except Exception as e:
            logger.error(f"Error generando resumen: {str(e)}")
            return {"summary": "Error al generar resumen", "error": str(e)}
