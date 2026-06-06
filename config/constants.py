"""
Constantes del proyecto
"""

# Estados de equipos
EQUIPMENT_STATES = {
    'OPERATIONAL': 'operativo',
    'MAINTENANCE': 'mantenimiento',
    'BROKEN': 'averiado',
    'SCHEDULED': 'mantenimiento_programado'
}

# Tipos de mantenimiento
MAINTENANCE_TYPES = {
    'PREVENTIVE': 'preventivo',
    'CORRECTIVE': 'correctivo',
    'PREDICTIVE': 'predictivo',
    'EMERGENCY': 'emergencia'
}

# Severidad de problemas
SEVERITY_LEVELS = {
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3,
    'CRITICAL': 4
}

# Tipos de equipos comunes
EQUIPMENT_TYPES = [
    'motor',
    'bomba',
    'compresor',
    'turbina',
    'generador',
    'transformador',
    'switchgear',
    'hvac',
    'electrobomba',
    'ventilador',
    'reductor',
    'rodamiento',
    'transmisión',
    'válvula',
    'tubería'
]

# Problemas comunes
COMMON_ISSUES = [
    'ruido_excesivo',
    'vibración',
    'sobrecalentamiento',
    'fuga',
    'corrosión',
    'desgaste',
    'desalineación',
    'desbalance',
    'cavitación',
    'contacto_eléctrico',
    'aislamiento_deficiente',
    'óxido',
    'problemas_lubricación',
    'erosión'
]

# API Endpoints
API_VERSION = 'v1'
API_BASE_PATH = f'/api/{API_VERSION}'

ENDPOINTS = {
    'CHATBOT': f'{API_BASE_PATH}/chatbot',
    'IMAGE_CLASSIFICATION': f'{API_BASE_PATH}/classify-image',
    'NLP_ANALYSIS': f'{API_BASE_PATH}/analyze-report',
    'PREDICTIONS': f'{API_BASE_PATH}/predictions',
    'LEARNING': f'{API_BASE_PATH}/learning',
    'EQUIPMENT': f'{API_BASE_PATH}/equipment',
    'ANALYTICS': f'{API_BASE_PATH}/analytics'
}

# Parámetros de modelos
MODEL_PARAMS = {
    'TEMPERATURE': 0.7,
    'MAX_TOKENS': 1024,
    'TOP_P': 0.95,
    'TOP_K': 40
}

# Límites de rate limiting
RATE_LIMITS = {
    'REQUESTS_PER_MINUTE': 60,
    'REQUESTS_PER_HOUR': 1000
}

# Configuración de imágenes
IMAGE_CONFIG = {
    'MAX_SIZE_MB': 10,
    'ALLOWED_FORMATS': ['jpg', 'jpeg', 'png', 'gif', 'webp'],
    'UPLOAD_TIMEOUT': 30
}
