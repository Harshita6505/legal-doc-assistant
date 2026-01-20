from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_DIR = "backend/vectorstore"
LLM_MODEL = "google/flan-t5-base"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL)

qa_pipeline = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    device=-1
)

def answer_question(question):
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectorstore = FAISS.load_local(VECTOR_DIR, embeddings, allow_dangerous_deserialization=True)

    docs = vectorstore.similarity_search(question, k=4)
    context = " ".join(doc.page_content for doc in docs)

    prompt = f"""
You are a legal assistant.
Answer ONLY using the context below.
If not found, say "Not mentioned in the document".

Context:
{context}

Question:
{question}
"""

    output = qa_pipeline(prompt, max_new_tokens=200, do_sample=False)
    return output[0]["generated_text"].strip()
