import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma

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

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent  

# Path to ChromaDB
CHROMA_DB_DIRECTORY = PROJECT_ROOT / "chroma_db"

def get_embedding_fn():
    """
    Returns the appropriate embedding function depending on your .env setting.
    """
    if USE_EMBEDDING_PROVIDER == "google":
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set but is required for Google embeddings.")
        # Configure Google Generative AI
        # genai.configure(api_key=GEMINI_API_KEY)
        # return GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    else:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set but is required for OpenAI embeddings.")
        return OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002")

def main():
    if not CHROMA_DB_DIRECTORY.exists():
        print(f"Error: ChromaDB directory '{CHROMA_DB_DIRECTORY}' not found. Have you created the database?")
        return

    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        user_query = input("Enter your query: ").strip()

    embedding_fn = get_embedding_fn()

    try:
        subtitlesdb = Chroma(
            persist_directory=str(CHROMA_DB_DIRECTORY),  
            embedding_function=embedding_fn
        )

        # Search for top 3 similar documents
    #    results = subtitlesdb.max_marginal_relevance_search(user_query, k=3, fetch_k=10)
        results = subtitlesdb.similarity_search(user_query, k=3)
        
        if not results:
            print("No results found for the query.")
            return
        
        for i, doc in enumerate(results, start=1):
            print(f"Result #{i}")
            print(doc.metadata['timestamp']) 
            print(doc.page_content)  
            print(f"{doc.metadata['link']}")  
            print("-----")

    except Exception as e:
        print(f"Error querying the database: {e}")



if __name__ == "__main__":
    main()