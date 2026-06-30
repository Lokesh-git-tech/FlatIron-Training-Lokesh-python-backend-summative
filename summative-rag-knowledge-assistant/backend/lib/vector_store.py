import chromadb

from langchain_ollama import OllamaEmbeddings

from config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    TOP_K,
)


embedding_model = OllamaEmbeddings(
    model=EMBEDDING_MODEL
)


client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)


collection = client.get_collection(
    COLLECTION_NAME
)


def retrieve_documents(question, top_k=TOP_K):
    """
    Retrieve the most relevant chunks from Chroma.
    """

    query_embedding = embedding_model.embed_query(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    retrieved_documents = []

    for document, metadata in zip(documents, metadatas):

        retrieved_documents.append(
            {
                "content": document,
                "title": metadata.get("title", ""),
                "path": metadata.get("path", ""),
            }
        )

    return retrieved_documents