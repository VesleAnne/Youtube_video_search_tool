from setuptools import setup, find_packages

setup(
    name="youtube_video_search_tool",
    version="0.1.0",
    author="Anna Simonova",
    author_email="vesleanne.gmail.com",
    description="A tool to download YouTube subtitles, store them in a vector database, and query video content using Gradio.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VesleAnne/Youtube_video_search_tool",
    packages=find_packages(),
    install_requires=[
        "gradio",    
        "chromadb",
        "selenium",
        "beautifulsoup4",
        "python-dotenv",
        "langchain",
        "openai"
    ],
    entry_points={
        "console_scripts": [
            "youtube-video-search=youtube_video_search_tool.gradio_app:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Unlicense",
        "Operating System :: OS Independent",
    ],
    license_files=["LICENSE"],
    python_requires='>=3.6',
)
