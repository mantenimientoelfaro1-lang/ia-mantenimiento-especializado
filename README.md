# 🤖 IA Especializada en Mantenimiento Técnico

## Descripción General

Sistema de inteligencia artificial con autoaprendizaje diseñado para asistir a técnicos especializados en mantenimiento. Integra múltiples capacidades de IA en Google Cloud Platform.

## 🎯 Características Principales

- ✅ **Chatbot Conversacional** - Diagnóstico de problemas técnicos
- ✅ **Clasificación de Imágenes** - Identificación de equipos y daños
- ✅ **Procesamiento de Lenguaje Natural** - Análisis de reportes
- ✅ **Análisis Predictivo** - Predicción de fallos
- ✅ **Autoaprendizaje** - Mejora continua con datos históricos

## 🛠️ Tecnologías

- **Cloud Platform**: Google Cloud Platform (GCP)
- **IA & ML**: Vertex AI, Vision API, Natural Language API
- **Backend**: Python 3.9+, Flask
- **Base de Datos**: BigQuery, Cloud Firestore
- **Almacenamiento**: Cloud Storage

## 📁 Estructura del Proyecto

```
ia-mantenimiento-especializado/
├── config/
│   ├── gcp_config.py
│   └── constants.py
├── models/
│   ├── chatbot_model.py
│   ├── image_classifier.py
│   ├── nlp_processor.py
│   └── prediction_model.py
├── api/
│   ├── app.py
│   ├── routes.py
│   └── middleware.py
├── services/
│   ├── vertex_ai_service.py
│   ├── vision_service.py
│   ├── nlp_service.py
│   └── bigquery_service.py
├── data/
│   ├── training_data/
│   └── historical_data/
├── tests/
│   ├── test_chatbot.py
│   ├── test_image_classifier.py
│   ├── test_nlp.py
│   └── test_predictions.py
├── docs/
│   ├── INSTALACION.md
│   ├── API.md
│   ├── ENTRENAMIENTO.md
│   └── ARQUITECTURA.md
├── requirements.txt
├── .env.example
├── .gitignore
├── setup.py
└── docker-compose.yml
```

## 🚀 Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/mantenimientoelfaro1-lang/ia-mantenimiento-especializado.git
cd ia-mantenimiento-especializado

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar credenciales GCP
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"

# Ejecutar
python api/app.py
```

## 📖 Documentación

- [Guía de Instalación](docs/INSTALACION.md)
- [API Reference](docs/API.md)
- [Guía de Entrenamiento](docs/ENTRENAMIENTO.md)
- [Arquitectura](docs/ARQUITECTURA.md)

## 📝 Licencia

MIT

## 👨‍💼 Autor

Mantenimiento El Faro
