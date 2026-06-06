"""
Configuración de Google Cloud Platform
"""
import os
from dotenv import load_dotenv
from google.auth import default
from google.cloud import aiplatform, vision, language_v1, bigquery, storage

load_dotenv()

class GCPConfig:
    """Configuración centralizada de GCP"""
    
    # Proyecto y región
    PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'tu-proyecto-gcp')
    REGION = os.getenv('GCP_REGION', 'us-central1')
    
    # Vertex AI
    VERTEX_AI_LOCATION = os.getenv('VERTEX_AI_LOCATION', 'us-central1')
    CHATBOT_MODEL_ID = os.getenv('CHATBOT_MODEL_ID', 'chat-bison')
    
    # BigQuery
    BIGQUERY_DATASET = os.getenv('BIGQUERY_DATASET', 'maintenance_ai')
    BIGQUERY_TABLE_PREDICTIONS = os.getenv('BIGQUERY_TABLE_PREDICTIONS', 'predictions')
    BIGQUERY_TABLE_ANALYTICS = os.getenv('BIGQUERY_TABLE_ANALYTICS', 'analytics')
    
    # Cloud Storage
    GCS_BUCKET = os.getenv('GCS_BUCKET', 'maintenance-ai-bucket')
    GCS_IMAGE_FOLDER = os.getenv('GCS_IMAGE_FOLDER', 'training_images')
    
    @staticmethod
    def initialize_clients():
        """Inicializa clientes de GCP"""
        credentials, project_id = default()
        
        clients = {
            'aiplatform': aiplatform.gapic.PredictionServiceClient(),
            'vision': vision.ImageAnnotatorClient(),
            'nlp': language_v1.LanguageServiceClient(),
            'bigquery': bigquery.Client(project=project_id),
            'storage': storage.Client(project=project_id),
        }
        
        return clients
    
    @staticmethod
    def get_vertex_ai_location_path(project: str, location: str) -> str:
        """Obtiene la ruta de ubicación de Vertex AI"""
        return f"projects/{project}/locations/{location}"


class DatabaseConfig:
    """Configuración de base de datos"""
    
    FIRESTORE_COLLECTION = os.getenv('FIRESTORE_COLLECTION', 'maintenance_records')
    FIRESTORE_SUBCOLLECTIONS = {
        'reports': 'maintenance_reports',
        'images': 'equipment_images',
        'predictions': 'failure_predictions',
        'learning': 'learning_data'
    }


class AppConfig:
    """Configuración de la aplicación"""
    
    ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')


class MLConfig:
    """Configuración del aprendizaje automático"""
    
    AUTO_LEARNING_ENABLED = os.getenv('AUTO_LEARNING_ENABLED', 'True').lower() == 'true'
    MODEL_UPDATE_FREQUENCY = os.getenv('MODEL_UPDATE_FREQUENCY', 'daily')
    MIN_CONFIDENCE = float(os.getenv('MIN_CONFIDENCE', '0.75'))
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', '32'))
    EPOCHS = int(os.getenv('EPOCHS', '10'))


class LoggingConfig:
    """Configuración de logging"""
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
