import os
import json
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

CHUNKS_FILE = "chunks.json"
CHROMA_DIR = "chroma_db"

def get_azure_openai_embeddings():
    load_dotenv()
    return AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
    )

def main():
    if not os.path.exists(CHUNKS_FILE):
        print(f"No se encontró {CHUNKS_FILE}. Ejecuta primero ingest.py.")
        return

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [chunk["text"] for chunk in chunks]
    metadatas = [{"source": chunk["source"], "chunk_id": chunk["chunk_id"]} for chunk in chunks]

    embeddings = get_azure_openai_embeddings()
    print("Generando embeddings y construyendo base vectorial...")
    db = Chroma.from_texts(
        texts,
        embeddings,
        metadatas=metadatas,
        persist_directory=CHROMA_DIR
    )
    db.persist()
    print(f"Base vectorial guardada en {CHROMA_DIR}")

if __name__ == "__main__":
    main()
