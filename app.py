import streamlit as st
import os
import tempfile

# If you already have backend functions, import them here
# from backend.pdf_loader import load_pdf
# from backend.search import semantic_search
# from backend.qa import answer_query

st.set_page_config(
    page_title="Legal Document Assistant",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Legal Document Assistant")
st.write("Upload legal documents and ask questions using AI-powered semantic search.")

# Session state
if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

if "docs_text" not in st.session_state:
    st.session_state.docs_text = ""

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("📂 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

process_btn = st.sidebar.button("📑 Process Documents")

# -------------------------------
# Document Processing
# -------------------------------
if process_btn and uploaded_files:
    with st.spinner("Processing documents..."):
        all_text = ""

        for pdf in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(pdf.read())
                tmp_path = tmp.name

            # ---- Replace this with your actual PDF loader ----
            # text = load_pdf(tmp_path)
            text = f"[Dummy text extracted from {pdf.name}]"
            all_text += text + "\n\n"

            os.remove(tmp_path)

        st.session_state.docs_text = all_text
        st.session_state.documents_loaded = True

    st.success("✅ Documents processed successfully!")

# -------------------------------
# Main Area
# -------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Document Preview")
    if st.session_state.documents_loaded:
        st.text_area(
            "Extracted Text",
            st.session_state.docs_text,
            height=400
        )
    else:
        st.info("Upload and process documents to preview content.")

with col2:
    st.subheader("❓ Ask a Question")
    query = st.text_input("Enter your legal question")

    ask_btn = st.button("🔍 Get Answer")

    if ask_btn:
        if not st.session_state.documents_loaded:
            st.warning("Please upload and process documents first.")
        elif query.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Generating answer..."):
                # ---- Replace with your real semantic search + LLM ----
                # results = semantic_search(query)
                # answer = answer_query(query, results)
                answer = f"Dummy answer for: '{query}'"

            st.markdown("### ✅ Answer")
            st.write(answer)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, FAISS & LLMs")
