import os
import fitz
import pickle
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

UPLOAD_DIR = "backend/data/uploads"
VECTOR_DIR = "backend/vectorstore"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

os.makedirs(VECTOR_DIR, exist_ok=True)

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    return " ".join(page.get_text() for page in doc)

def ingest_pdf(pdf_path):
    text = extract_text(pdf_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )

    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectorstore = FAISS.from_texts(chunks, embeddings)

    vectorstore.save_local(VECTOR_DIR)

    with open(f"{VECTOR_DIR}/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print("✅ PDF ingested & FAISS index saved")
