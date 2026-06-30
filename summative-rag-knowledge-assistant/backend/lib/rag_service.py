import requests

from config import (
    LLM_MODEL,
    OLLAMA_BASE_URL,
)

from lib.vector_store import retrieve_documents


def ask_question(question):
    """
    Runs the Retrieval-Augmented Generation (RAG) workflow.

    Steps:
    1. Retrieve relevant documents.
    2. Build context.
    3. Send prompt to Ollama.
    4. Return answer with supporting sources.
    """

    documents = retrieve_documents(question)

    # Fallback if nothing relevant was found
    if len(documents) == 0:

        return {
            "answer": (
                "I do not have enough information in the provided knowledge base "
                "to answer your question."
            ),
            "sources": [],
            "metadata": {
                "model": LLM_MODEL,
                "retrieved_chunks": 0,
            },
        }

    # Build context for the model
    context = ""

    for document in documents:

        context += document["content"]
        context += "\n\n"

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the information provided in the context below.

If the answer cannot be found in the context,
reply that you do not have enough information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()

    result = response.json()

    answer = result.get("response", "").strip()

    sources = []

    for document in documents:

        excerpt = document["content"]

        if len(excerpt) > 250:
            excerpt = excerpt[:250] + "..."

        sources.append(
            {
                "title": document["title"],
                "content": excerpt,
                "metadata": {
                    "path": document["path"],
                },
            }
        )

    return {
        "answer": answer,
        "sources": sources,
        "metadata": {
            "model": LLM_MODEL,
            "retrieved_chunks": len(documents),
        },
    }