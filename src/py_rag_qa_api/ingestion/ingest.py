from psycopg2.extras import execute_values
import numpy as np
from sentence_transformers import SentenceTransformer
from py_rag_qa_api.vectordb.store import connect
from py_rag_qa_api.config.settings import create_config

model = SentenceTransformer("all-MiniLM-l6-v2")

text_file_path = "D:/Belajar/Pemrograman/Latihan/py-rag-qa-api/datasets/cat-facts.txt"

with open(text_file_path, "r", encoding="utf-8") as f:
    text = f.read()
print("dataset loaded")

def split_text(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0
    chunk_number = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        chunk_number += 1
        print(f"{chunk_number} chunk added to chunks")
        start += chunk_size - overlap
    return chunks

chunks = split_text(text=text)
print("dataset splitted")

embeddings = model.encode(chunks)
print("chunks embedded")


cfg = create_config()

conn = connect(cfg=cfg)

cur = conn.cursor()

data_to_insert = [
    (chunk, embedding.tolist())
    for chunk, embedding in zip(chunks, embeddings)
]

try:
    execute_values(
        cur,
        "INSERT INTO cat_facts (content, embedding) VALUES %s",
        data_to_insert
    )
    conn.commit()
    cur.close()
    conn.close()
    print("dataset added to vector database")
except Exception as e:
    print(f"dataset failed to added to vector database: {e}")