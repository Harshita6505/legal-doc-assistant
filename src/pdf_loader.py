import os
import json
from pypdf import PdfReader

# =========================================================
# PATH SETUP (robust, works regardless of where script runs)
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_PDF_DIR = os.path.join(BASE_DIR, "data", "raw_pdfs")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)

PDF_FILE = os.path.join(RAW_PDF_DIR, "sample.pdf")
CLEANED_TEXT_FILE = os.path.join(PROCESSED_DIR, "sample_cleaned.txt")
CHUNKS_FILE = os.path.join(PROCESSED_DIR, "sample_chunks.json")

# =========================================================
# STEP 1: LOAD PDF
# =========================================================

def load_pdf_text(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at: {pdf_path}")

    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

# =========================================================
# STEP 2: CLEAN LEGAL TEXT
# =========================================================

def clean_legal_text(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

# =========================================================
# STEP 3: CHUNK TEXT FOR SEMANTIC SEARCH
# =========================================================

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + chunk_size, length)
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

# =========================================================
# MAIN PIPELINE
# =========================================================

if __name__ == "__main__":

    print("🚀 Starting PDF processing pipeline...")

    # Load PDF
    pdf_text = load_pdf_text(PDF_FILE)

    # Clean text
    cleaned_text = clean_legal_text(pdf_text)

    # Save cleaned text
    with open(CLEANED_TEXT_FILE, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    # Chunk text
    chunks = chunk_text(cleaned_text)

    # Save chunks
    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    # Logs
    print("✅ PDF processed successfully")
    print(f"📄 Input PDF: {PDF_FILE}")
    print(f"📁 Cleaned text saved to: {CLEANED_TEXT_FILE}")
    print(f"🧩 Total chunks created: {len(chunks)}")
    print(f"📦 Chunks saved to: {CHUNKS_FILE}")
    print("🔍 Sample chunk preview:")
    print(chunks[0][:300])
