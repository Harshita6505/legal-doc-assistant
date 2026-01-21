import streamlit as st
import requests

st.set_page_config(page_title="Legal Doc Assistant", layout="centered")

st.title("📄 Legal Document Assistant")
st.write("Upload a legal document and get a concise AI-generated summary.")

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"  # change if needed

uploaded_file = st.file_uploader(
    "Upload a legal document",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    st.success("File uploaded successfully")

    if st.button("Summarize Document"):
        with st.spinner("Processing document..."):
            files = {"file": uploaded_file}
            response = requests.post(
                f"{BACKEND_URL}/summarize",
                files=files
            )

        if response.status_code == 200:
            summary = response.json().get("summary")
            st.subheader("📌 Summary")
            st.write(summary)
        else:
            st.error("Failed to summarize document")
