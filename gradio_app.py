import gradio as gr
import subprocess
from pathlib import Path
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).parent
SRC_DIR = SCRIPT_DIR / "src"

load_dotenv(".env")

def is_url(text: str) -> bool:
    """
    Checks if the user passes a YouTube url to process or not.
    If a string is a YouTube  url it returns True, otherwise it returns False.
    """
    return text.startswith("https://www.youtube.com") or text.startswith("https://youtu.be")

def process_input(user_input: str) -> str:
    """
    If user input is a YouTube URL, parses it (downloads subs, builds DB),
    otherwise treats it as a query to the DB.
    Returns a response string.
    To do: Need to add a check if the query is a url but not YouTube. 
    """
    user_input = user_input.strip()

    if not user_input:
        return "Please enter a YouTube URL or a query.", gr.update(value="❌ No input provided.")

    if is_url(user_input):
        try:
            # Call parser.py to process the link
            result = subprocess.run(["python3", str(SRC_DIR / "parser.py"), user_input], capture_output=True, text=True)
            if result.returncode != 0:
                return f"Error parsing URL: {result.stderr}"

            # Call create_database.py to update the database
            result = subprocess.run(["python3", str(SRC_DIR / "create_database.py")], capture_output=True, text=True)
            if result.returncode != 0:
                return f"Error updating database: {result.stderr}"

            return "Link parsed successfully. Subtitles downloaded and database updated."

        except Exception as e:
            return f"Error processing link: {e}"
    
    else:
        try:
            # Call query.py to search the database
            result = subprocess.run(["python3", str(SRC_DIR / "query.py"), user_input], capture_output=True, text=True)
            if result.returncode != 0:
                return f"Error querying the database: {result.stderr}"
            
            return result.stdout.strip()

        except Exception as e:
            return f"Error processing query: {e}"
        
# Gradio Interface

with gr.Blocks() as demo:
    gr.Markdown("## 📺 YouTube Video Search tool")

    with gr.Row():
        user_input = gr.Textbox(
            lines=1,
            label="Enter a YouTube URL to a single video or a channel or a Query to the existing video database",
            placeholder="e.g. https://www.youtube.com/watch?v=..., or 'Harry Potter'"
        )
    output_box = gr.Textbox(
        label="Output",
        lines=10
    )

    submit_button = gr.Button("Submit")

    submit_button.click(fn=process_input, inputs=user_input, outputs=output_box)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)