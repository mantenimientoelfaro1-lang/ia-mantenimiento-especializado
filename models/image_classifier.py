"""
Módulo de Clasificación de Imágenes con Vision API
"""
import logging
from typing import Dict, List, Tuple, Optional
from PIL import Image
import io
from google.cloud import vision
from google.cloud import storage
from config.gcp_config import GCPConfig
from config.constants import EQUIPMENT_TYPES, IMAGE_CONFIG

logger = logging.getLogger(__name__)


class ImageClassifier:
    """Clasificador de imágenes de equipos para mantenimiento"""
    
    def __init__(self):
        """Inicializa el clasificador de imágenes"""
        self.vision_client = vision.ImageAnnotatorClient()
        self.storage_client = storage.Client()
        self.bucket_name = GCPConfig.GCS_BUCKET
        self.equipment_types = EQUIPMENT_TYPES
        logger.info("Clasificador de imágenes inicializado")
    
    def classify_equipment_image(self, image_path: str) -> Dict:
        """
        Clasifica una imagen de equipo de mantenimiento
        
        Args:
            image_path: Ruta local o URL de la imagen
            
        Returns:
            Diccionario con clasificación y metadatos
        """
        try:
            # Leer imagen
            image_content = self._read_image(image_path)
            
            # Realizar análisis de visión
            analysis_result = self._analyze_image(image_content)
            
            # Clasificar equipos detectados
            classification = self._classify_equipment(analysis_result)
            
            # Detectar problemas
            problems = self._detect_problems(analysis_result)
            
            return {
                "success": True,
                "equipment_detected": classification,
                "problems_detected": problems,
                "confidence": analysis_result.get("confidence", 0),
                "labels": analysis_result.get("labels", [])
            }
            
        except Exception as e:
            logger.error(f"Error clasificando imagen: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _read_image(self, image_path: str) -> bytes:
        """
        Lee una imagen desde archivo local o URL
        
        Args:
            image_path: Ruta de la imagen
            
        Returns:
            Contenido de la imagen en bytes
        """
        if image_path.startswith(('http://', 'https://')):
            return vision.Image(source=vision.ImageSource(image_uri=image_path))
        else:
            with open(image_path, 'rb') as f:
                return f.read()
    
    def _analyze_image(self, image_content: bytes) -> Dict:
        """
        Realiza análisis de visión computacional
        
        Args:
            image_content: Contenido de la imagen
            
        Returns:
            Resultado del análisis
        """
        try:
            # Crear imagen para Vision API
            if isinstance(image_content, bytes):
                image = vision.Image(content=image_content)
            else:
                image = image_content
            
            # Realizar diferentes tipos de análisis
            label_response = self.vision_client.label_detection(image=image)
            object_response = self.vision_client.object_localization(image=image)
            text_response = self.vision_client.text_detection(image=image)
            
            return {
                "labels": [
                    {"name": label.description, "confidence": label.score}
                    for label in label_response.label_annotations
                ],
                "objects": [
                    {
                        "name": obj.name,
                        "confidence": obj.score,
                        "vertices": [(v.x, v.y) for v in obj.bounding_poly.normalized_vertices]
                    }
                    for obj in object_response.localized_object_annotations
                ],
                "text": text_response.text_annotations[0].description if text_response.text_annotations else "",
                "confidence": label_response.label_annotations[0].score if label_response.label_annotations else 0
            }
            
        except Exception as e:
            logger.error(f"Error en análisis de imagen: {str(e)}")
            raise
    
    def _classify_equipment(self, analysis_result: Dict) -> List[Dict]:
        """
        Clasifica los equipos detectados en la imagen
        
        Args:
            analysis_result: Resultado del análisis de visión
            
        Returns:
            Lista de equipos clasificados
        """
        detected_equipment = []
        
        for label in analysis_result.get("labels", []):
            label_name = label["name"].lower()
            
            # Buscar equipos coincidentes
            for equipment_type in self.equipment_types:
                if equipment_type in label_name or label_name in equipment_type:
                    detected_equipment.append({
                        "type": equipment_type,
                        "confidence": label["confidence"],
                        "detected_label": label["name"]
                    })
                    break
        
        return detected_equipment
    
    def _detect_problems(self, analysis_result: Dict) -> List[Dict]:
        """
        Detecta posibles problemas visuales en el equipo
        
        Args:
            analysis_result: Resultado del análisis de visión
            
        Returns:
            Lista de problemas detectados
        """
        problems = []
        labels_lower = [l["name"].lower() for l in analysis_result.get("labels", [])]
        
        # Palabras clave para detectar problemas
        problem_keywords = {
            "corrosion": "corrosión",
            "rust": "óxido",
            "leak": "fuga",
            "damage": "daño",
            "crack": "grieta",
            "burn": "quemadura",
            "deformation": "deformación",
            "displacement": "desplazamiento",
            "broken": "roto"
        }
        
        for keyword, problem in problem_keywords.items():
            for label in labels_lower:
                if keyword in label:
                    problems.append({
                        "type": problem,
                        "detected_in": label,
                        "severity": "high"
                    })
        
        return problems
    
    def upload_image_to_gcs(self, image_path: str, destination_blob_name: str) -> bool:
        """
        Sube una imagen a Google Cloud Storage
        
        Args:
            image_path: Ruta local de la imagen
            destination_blob_name: Nombre en GCS
            
        Returns:
            True si fue exitoso
        """
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(image_path)
            logger.info(f"Imagen subida a GCS: {destination_blob_name}")
            return True
        except Exception as e:
            logger.error(f"Error subiendo imagen a GCS: {str(e)}")
            return False
    
    def batch_classify_images(self, image_paths: List[str]) -> List[Dict]:
        """
        Clasifica múltiples imágenes en lote
        
        Args:
            image_paths: Lista de rutas de imágenes
            
        Returns:
            Lista de resultados de clasificación
        """
        results = []
        for image_path in image_paths:
            result = self.classify_equipment_image(image_path)
            results.append({"image": image_path, **result})
        return results
