import os
import re
import pandas as pd
from pathlib import Path
import google.generativeai as genai
from langchain_chroma import Chroma

from langchain.schema import Document
from langchain_openai.embeddings import OpenAIEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent 

load_dotenv(ROOT_DIR / '.env')

genai.configure(api_key='GEMINI_API_KEY')

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
USE_EMBEDDING_PROVIDER = os.getenv("USE_EMBEDDING_PROVIDER", "openai").strip().lower()

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent
SUBTITLES_FOLDER = SCRIPT_DIR.parent / "subtitles"
CHROMA_DB_DIRECTORY = PROJECT_ROOT / "chroma_db"
METADATA_FILE = "subtitles_metadata.csv"

SUBTITLES_FOLDER.mkdir(parents=True, exist_ok=True)
CHROMA_DB_DIRECTORY.mkdir(parents=True, exist_ok=True)

def parse_srt_file(file_path):
    """
    Parses an srt file and extracts subtitles with timestamps.
    Returns a list of dictionaries with the video_id, timestamp, text, and link.
    """
    video_id = Path(file_path).stem
    subtitles = []
    
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    blocks = content.strip().split("\n\n")
    for block in blocks:
        lines = block.split("\n")
        if len(lines) >= 3:
            try:
                timestamp_line = lines[1]
                start_time_match = re.search(r"\((\d+)\)", timestamp_line)
                if start_time_match:
                    start_time = int(start_time_match.group(1))  
                else:
                    raise ValueError(f"Invalid timestamp line: {timestamp_line}")
                visible_timestamp = timestamp_line.split(" (")[0]
                text = " ".join(lines[2:])
                link = f"https://youtu.be/{video_id}?t={start_time}"

                subtitles.append({
                    "video_id": video_id,
                    "start_time": start_time,
                    "timestamp": visible_timestamp,
                    "text": text,
                    "link": link
                })            
                
            except Exception as e:
                print(f"Error parsing block: {block}\n{e}")
    return subtitles


def main():
    try:
        if not SUBTITLES_FOLDER.exists():
            print(f"Folder '{SUBTITLES_FOLDER}' does not exist.")
            return
        
        print("All files in 'subtitles':", list(SUBTITLES_FOLDER.glob("*.srt")))

        all_subtitles = []
        for file in SUBTITLES_FOLDER.glob("*.srt"):
            print("Found SRT file:", file.name)
            subtitles = parse_srt_file(file)
            all_subtitles.extend(subtitles)

        if not all_subtitles:
            print("No subtitles found to process.")
            return
        
        metadata = pd.DataFrame(all_subtitles)
        metadata.to_csv(METADATA_FILE, index=False)
        print(f"Saved metadata to {METADATA_FILE}")

        # Prepare documents for ChromaDB
        documents = [
            Document(page_content=item["text"], metadata={
                "video_id": item["video_id"],
                "start_time": item["start_time"],
                "timestamp": item["timestamp"],
                "link": item["link"]
            })
            for item in all_subtitles
        ]

        # Choose Embedding Provider
        if USE_EMBEDDING_PROVIDER == "google":
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            
            if not GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY is not set in .env but is required for Google embeddings.")
            
            genai.configure(api_key=GEMINI_API_KEY)
            embedding_fn = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
            print("Using Google Generative AI for embeddings.")
        
        else:
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is not set in .env but is required for OpenAI embeddings.")
            
            embedding_fn = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
            print("Using OpenAI for embeddings.")

        # Load or create ChromaDB outside 'src'
        if CHROMA_DB_DIRECTORY.exists():
            print("Updating existing Chroma database...")
            subtitlesdb = Chroma(persist_directory=str(CHROMA_DB_DIRECTORY), embedding_function=embedding_fn)
            subtitlesdb.add_documents(documents)
        else:
            print("Creating a new Chroma database...")
            subtitlesdb = Chroma.from_documents(
                documents=documents,
                embedding=embedding_fn,
                persist_directory=str(CHROMA_DB_DIRECTORY)
            )
        
        print("Data successfully saved to Chroma DB.")

        # Delete processed srt files
        for srt_file in SUBTITLES_FOLDER.glob("*.srt"):
            try:
                srt_file.unlink()
                print(f"Deleted file: {srt_file.name}")
            except Exception as e:
                print(f"Could not delete file {srt_file.name}: {e}")

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    main()
