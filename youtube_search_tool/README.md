# YouTube Search Tool

Search and query YouTube videos using AI embeddings. Add individual videos or entire channels, then search through their content using natural language.

## Features

- 🎥 Process individual YouTube videos or entire channels
- 🔍 Semantic search through video transcripts  
- 🤖 Multiple AI providers (OpenAI, Google, Local models)
- 🌐 Web interface with Gradio
- ⚡ Fast batch processing with concurrent downloads
- 🐳 Docker support for easy deployment

## Installation Options

### Option 1: Install with pip

```bash
pip install youtube-search-tool-using-subtitles
```

### Option 2: Install with Docker

```bash
# Clone or download the project
git clone https://github.com/VesleAnne/Youtube_video_search_tool.git
cd youtube-search-tool

# Run with Docker Compose (recommended)
docker-compose up
```

## Quick Start

### 1. Set up environment

**For pip installation:**
Create a `.env` file in your working directory:

**For Docker:**
Copy the example environment file:
```bash
cp .env.example .env
```

Then edit `.env` with your settings:
```bash
# Choose your AI provider
USE_EMBEDDING_PROVIDER=openai  # or 'google' or 'local'
USE_LLM_PROVIDER=openai

# API Keys 
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_google_key_here

# Optional: Customize processing
MAX_WORKERS=4
MAX_CHANNEL_VIDEOS=100
```

### 2. Run the application

**With pip (Command Line):**
```bash
# Add a single video
yt-search add "https://www.youtube.com/watch?v=QPM0WNqwJBc"

# Add an entire channel
yt-search add "https://www.youtube.com/@Lamediainglesa"

# Search through your videos
yt-search search "Voldemort"

# Launch web interface
yt-search web
```

**With pip (Web Interface Only):**
```bash
python -c "import gradio as gr; exec(open('gradio_app.py').read())" 
```

**With Docker:**
```bash
# Start the application
docker-compose up

# Access web interface at http://localhost:7860
```

**Docker management commands:**
```bash
# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Rebuild after changes
docker-compose up --build
```

### 3. Using the Web Interface

1. **Choose AI Provider**: Select OpenAI, Google, or Local models
2. **Add Videos**: Paste YouTube URLs (videos or channels)
3. **Search**: Enter natural language queries to find content
4. **Results**: View top 3 matches with timestamps and direct links

## Requirements

### For pip installation:
- Python 3.8+
- Chrome/Chromium browser (for channel scraping)

### For Docker installation:
- Docker and Docker Compose
- 2GB+ available disk space

## Supported AI Providers

- **OpenAI**: `text-embedding-ada-002` (requires API key)
- **Google**: `text-embedding-004` (requires API key)  
- **Local**: `all-MiniLM-L6-v2` (no API key needed, slower)

## Examples

### Adding Content
```bash
# Single video
yt-search add "https://www.youtube.com/watch?v=QPM0WNqwJBc"

# Entire channel (will process up to 100 videos by default)
yt-search add "https://www.youtube.com/@Lamediainglesa"


```

### Searching
```bash
# Example queries  
yt-search search "Premier League best goals"
yt-search search "Manchester United transfer news"
yt-search search "Liverpool vs Arsenal highlights"
yt-search search "English football tactics analysis"
```

## Data Persistence

### Pip Installation:
Data is stored in your current working directory:
- `chroma_db/` - Vector database
- `models/` - Downloaded AI models
- `cache/` - Processed results cache

### Docker Installation:
Data is automatically persisted in Docker volumes and local directories.

## Troubleshooting

**Chrome/ChromeDriver issues:**
- Ensure Chrome is installed and up to date
- For Docker: Chrome is automatically installed in the container

**API Key errors:**
- Check your `.env` file has correct API keys
- Verify API keys are valid and have sufficient credits

**Memory issues:**
- Reduce `MAX_CHANNEL_VIDEOS` for large channels
- Use local models if you have limited API credits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both pip and Docker installations
5. Submit a pull request

## License

MIT License - see [LICENSE] file for details.
