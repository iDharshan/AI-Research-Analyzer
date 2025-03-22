from fastapi import FastAPI
import gradio as gr
from dotenv import load_dotenv
import os
from app.utils import ui_interface

# Load environment variables
load_dotenv()

# Create Gradio interface
demo = gr.Interface(
    fn=ui_interface,
    inputs=[
        gr.File(label="Upload PDF", file_types=[".pdf"]), 
        gr.Radio(["Key Insights", "Research Gaps"], label="Choose Query Type", value="Key Insights")
    ],
    outputs=[
        gr.Markdown(label="Response"), 
        gr.Textbox(label="Sources")
    ],
    title="Research Paper Analyzer",
    description="Upload a research paper and extract key insights or research gaps using RAG."
)

# Create FastAPI app and mount Gradio
app = FastAPI(title="Research Paper Analyzer API")
app = gr.mount_gradio_app(app, demo, path="/")

# Define a function to run the server that can be imported by other modules
def run_server(host="127.0.0.1", port=8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)

# This allows the file to be run directly for development
if __name__ == "__main__":
    run_server()