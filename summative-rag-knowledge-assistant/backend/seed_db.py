import os

import chromadb

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    KNOWLEDGE_BASE_PATH,
)


embedding_model = OllamaEmbeddings(
    model=EMBEDDING_MODEL
)

client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)

try:
    client.delete_collection(COLLECTION_NAME)
except Exception:
    pass

collection = client.create_collection(COLLECTION_NAME)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

documents = []

for filename in os.listdir(KNOWLEDGE_BASE_PATH):

    if filename.endswith(".md"):

        filepath = os.path.join(
            KNOWLEDGE_BASE_PATH,
            filename,
        )

        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()

        chunks = splitter.split_text(text)

        for index, chunk in enumerate(chunks):

            documents.append(
                {
                    "id": f"{filename}-{index}",
                    "text": chunk,
                    "title": filename,
                    "path": filepath,
                }
            )

print(f"Loaded {len(documents)} chunks.")

for document in documents:

    embedding = embedding_model.embed_query(
        document["text"]
    )

    collection.add(
        ids=[document["id"]],
        embeddings=[embedding],
        documents=[document["text"]],
        metadatas=[
            {
                "title": document["title"],
                "path": document["path"],
            }
        ],
    )

print("Knowledge base indexed successfully.")