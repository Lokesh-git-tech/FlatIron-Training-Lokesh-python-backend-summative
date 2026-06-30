import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KNOWLEDGE_BASE_PATH = os.path.join(BASE_DIR, "knowledge_base")

CHROMA_DB_PATH = os.getenv(
    "CHROMA_DB_PATH",
    os.path.join(BASE_DIR, "chroma_db"),
)

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "knowledge_base",
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "embeddinggemma",
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "llama3.2",
)

TOP_K = int(
    os.getenv(
        "TOP_K",
        "3",
    )
)