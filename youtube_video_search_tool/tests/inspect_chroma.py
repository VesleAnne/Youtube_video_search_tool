import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from langchain_openai.embeddings import OpenAIEmbeddings
# If using Google GenAI:
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# import google.generativeai as genai

# Load environment variables from .env
load_dotenv(".env")

# Read keys and embedding choice
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
USE_EMBEDDING_PROVIDER = os.getenv("USE_EMBEDDING_PROVIDER", "openai").strip().lower()

# Directory where your Chroma DB is stored
CHROMA_DB_DIRECTORY = "chroma_db"

def main():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is missing in your environment.")

    embedding_fn = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-ada-002")

    vectorstore = Chroma(
        embedding_function=embedding_fn,
        persist_directory=CHROMA_DB_DIRECTORY
    )

    data = vectorstore._collection.get(include=["documents", "metadatas"])
    docs = data["documents"]
    metas = data["metadatas"]

    print(f"Found {len(docs)} documents in Chroma.\n")
    for i, (doc, meta) in enumerate(zip(docs, metas), start=1):
        print(f"=== Document #{i} ===")
        print("Text:", doc)
        print("Metadata:", meta)
        print()

if __name__ == "__main__":
    main()