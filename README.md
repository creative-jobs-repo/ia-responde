# IA Responde (Isaac Asimov Responde)

Hazle preguntas a los textos de Isaac Asimov y obtén respuestas basadas en sus propias palabras.

## Instalación

```bash
git clone <URL-del-repo>
cd ia-responde-mvp
pip install -r requirements.txt
```

## Configuración para Azure OpenAI

1. Obtén tu endpoint, API key y nombre de deployment/modelo en Azure OpenAI.
2. Crea un archivo `.env` en la raíz con:

```
AZURE_OPENAI_API_KEY=tu-api-key
AZURE_OPENAI_ENDPOINT=https://<tu-endpoint>.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=nombre-del-deployment
AZURE_OPENAI_API_VERSION=2023-05-15
```

## Uso

1. Coloca tus PDFs en la carpeta `pdfs/`
2. Ejecuta `python ingest.py` para extraer y chunkear los textos.
3. Ejecuta `python build_db.py` para generar los embeddings y construir la base vectorial.
4. Inicia la API: `uvicorn main:app --reload`
5. Haz preguntas vía POST a `/ask` con el campo `question`.

## Ejemplo de consulta

```bash
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{"question": "¿Qué opina Asimov sobre la inteligencia artificial?"}'
```

## Dependencias

Ver `requirements.txt`.

## Licencia

MIT
