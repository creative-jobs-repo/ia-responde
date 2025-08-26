import os
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

PDF_DIR = "pdfs"
OUTPUT_FILE = "chunks.json"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def main():
    all_chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    for filename in os.listdir(PDF_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, filename)
            print(f"Procesando {pdf_path}...")
            text = extract_text_from_pdf(pdf_path)
            chunks = splitter.split_text(text)
            for i, chunk in enumerate(chunks):
                all_chunks.append({
                    "source": filename,
                    "chunk_id": i,
                    "text": chunk
                })
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    print(f"Guardados {len(all_chunks)} chunks en {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
