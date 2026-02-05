from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)
    return chunks
