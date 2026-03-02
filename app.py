import streamlit as st
from transformers import pipeline
import PyPDF2

# ---------------------------
# Load summarization model
# ---------------------------
@st.cache_resource
def load_model():
    return pipeline("summarization", model="t5-small")

summarizer = load_model()

# ---------------------------
# Extract text from PDF
# ---------------------------
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# ---------------------------
# Summarize text
# ---------------------------
def summarize_text(text):
    max_chunk = 500  # T5-small limit
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    
    summary = ""
    for chunk in chunks[:5]:  # limit for speed
        result = summarizer(chunk, max_length=120, min_length=40, do_sample=False)
        summary += result[0]['summary_text'] + "\n"
    
    return summary

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Legal Document Summarizer", layout="centered")

st.title("⚖️ Legal Document Summarizer")
st.write("Upload a legal PDF and get a quick summary.")

uploaded_file = st.file_uploader("Upload Legal PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading PDF..."):
        text = extract_text_from_pdf(uploaded_file)

    if text.strip():
        st.success("PDF loaded successfully!")

        if st.button("Generate Summary"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(text)

            st.subheader("📄 Summary")
            st.write(summary)

            # Optional: show raw text
            with st.expander("View extracted text"):
                st.write(text[:5000])
    else:
        st.error("Could not extract text from this PDF.")