# AI Research Paper Insight & Gap Identifier – RAG, Sentence Transformers, FastAPI & Gradio

A web application that uses Retrieval-Augmented Generation (RAG) to analyze research papers and extract key insights or identify research gaps.

![Research Paper Analyzer](https://user-images.githubusercontent.com/your-username/your-repo-name/raw/main/screenshots/app-screenshot.png)

## Features

- **PDF Analysis**: Upload any research paper in PDF format
- **Key Insights Extraction**: Automatically identify and summarize the main findings
- **Research Gaps Detection**: Highlight limitations and areas for future research
- **User-Friendly Interface**: Simple web UI powered by Gradio
- **API Access**: FastAPI backend allows programmatic access

## Technology Stack

- **FastAPI**: Modern, high-performance web framework
- **Gradio**: Simple UI for machine learning models
- **LangChain**: Framework for LLM applications
- **Azure OpenAI**: Powerful language model integration
- **FAISS**: Vector similarity search for document retrieval
- **HuggingFace Embeddings**: Sentence transformers for text representation

## Getting Started

### Prerequisites

- Python 3.9+
- Azure OpenAI API access

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/AI-Research-Analyzer.git
   cd AI-Research-Analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env .env
   # Edit .env with your Azure OpenAI API key and endpoint
   ```

### Running the Application

Run the application with:

```bash
python -m app.main
```

The application will be available at http://127.0.0.1:8000

## Usage

1. Access the web interface at http://127.0.0.1:8000
2. Upload a research paper in PDF format
3. Select analysis type: "Key Insights" or "Research Gaps"
4. View the generated analysis

## How It Works

The application uses a Retrieval-Augmented Generation (RAG) architecture:

1. **Document Processing**: PDFs are loaded and split into manageable chunks
2. **Vector Embedding**: Text chunks are converted to vector embeddings
3. **Retrieval**: When a query is made, relevant chunks are retrieved
4. **Generation**: Retrieved content is sent to the LLM with a specialized prompt
5. **Response**: A structured analysis is returned to the user

## Future Improvements

- Support for additional document formats (DOCX, TXT)
- Batch processing of multiple papers
- More analysis types (methodology critique, literature comparison)
- Visualization of document relationships and key concepts

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- Powered by Azure OpenAI models
- Interface created with [Gradio](https://gradio.app/)
