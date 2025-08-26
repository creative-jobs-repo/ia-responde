import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.vectorstores import Chroma
from langchain.llms import AzureOpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings import AzureOpenAIEmbeddings
from dotenv import load_dotenv

CHROMA_DIR = "chroma_db"

load_dotenv()

class AskRequest(BaseModel):
    question: str

def get_qa_chain():
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
    )
    db = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    retriever = db.as_retriever()
    llm = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
    )
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa

app = FastAPI()
qa_chain = get_qa_chain()

@app.post("/ask")
def ask(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")
    result = qa_chain(request.question)
    answer = result["result"]
    sources = [
        {
            "source": doc.metadata.get("source"),
            "chunk_id": doc.metadata.get("chunk_id")
        }
        for doc in result.get("source_documents", [])
    ]
    return {"answer": answer, "sources": sources}
