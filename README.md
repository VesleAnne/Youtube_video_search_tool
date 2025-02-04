# 🎬 YouTube Video search engine with Gradio interface

**A Python-based tool that downloads subtitles from YouTube videos, stores them in a vector database (ChromaDB), and allows users to query video content using Gradio. It returns three closest answers with the links to the exact moments in the video where the phrases are.**  


## **How it works**
You can pass a link to a YouTube video or the entire channel. The script then will download subtitles for the video (videos) and store them in a vector database. Then you may make queries to the database to find the exact moment on the video without the need to rewatch it. 
Note: by default the script downloads subtitles for 120 latest videos on the channel. If you want to change this number, please, go to selenium_parser.py and change the number of scroll downs of the page. The more video you pass at once the longer they will be processed. It takes 12-15 seconds to process one video.
The script uses GPT or Gemini to create embeddings but it can be changed to use any other model you like. To change this go to create_databse.py
By default script returns 3 closest answers to the query. You may change this number in the script query.py 

## **Installation**

1️⃣  **Clone the Repository**

git clone https://github.com/your-username/your-repo.git
cd your-repo

2️⃣  **Create a Virtual Environment**

python3 -m venv youtubeenv

source youtubeenv/bin/activate  # for Mac/Linux
youtubeenv\Scripts\activate   # for Windows

3️⃣  **Install Dependencies**

pip install -r requirements.txt

4️⃣  **Set Up API Keys**

Create a .env file in the project root and add:

OPENAI_API_KEY="your-openai-key"
or 
GEMINI_API_KEY="your-google-gemini-key

## Usage

Run the Gradio Interface:

python3 src/gradio_app.py

- Enter a YouTube video or channel URL to download subtitles.
- Enter a query to search subtitles in the database.
- Click Submit to get results.