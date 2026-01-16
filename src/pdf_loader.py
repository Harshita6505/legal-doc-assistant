from pypdf import PdfReader
from pathlib import Path

def load_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


if __name__ == "__main__":
    pdf_path = Path("../data/raw_pdfs/sample.pdf")
    content = load_pdf_text(pdf_path)
    print(content[:1000])
