import pickle
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

LLM_MODEL = "google/flan-t5-base"
VECTOR_DIR = "backend/vectorstore"

tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL)

summarizer = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    device=-1
)

def summarize_document():
    with open(f"{VECTOR_DIR}/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    partial_summaries = []

    for chunk in chunks[:10]:
        prompt = f"Summarize this legal text:\n{chunk}"
        out = summarizer(prompt, max_new_tokens=120, do_sample=False)
        partial_summaries.append(out[0]["generated_text"])

    final_prompt = "Combine into a clear legal summary:\n" + " ".join(partial_summaries)
    final = summarizer(final_prompt, max_new_tokens=200, do_sample=False)

    return final[0]["generated_text"].strip()
