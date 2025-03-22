import os
import tempfile
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

# Initialize models
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = AzureChatOpenAI(
    model="gpt-4o-mini", 
    api_key=azure_api_key, 
    azure_endpoint=azure_endpoint, 
    api_version="2024-10-21"
)

# Prompt templates
key_insights_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""Extract the key insights from the given document. 
    
Document content: 
{context}

For your response:
1. Start with a brief 2-3 sentence summary of what the document is about
2. List 5-8 key insights with clear headings and brief explanations
3. For each insight, include a short explanation of its significance
4. End with a one-paragraph conclusion connecting these insights

Format each insight as:
## [Insight Title]
[1-2 sentences explaining the insight]
[1 sentence about why this matters]

Query: {question}
""")

research_gaps_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""Identify research gaps or limitations in the given document.

Document content:
{context}

For your response:
1. Begin with a brief overview of the document's focus (2-3 sentences)
2. Identify 4-6 significant research gaps or limitations
3. For each gap:
   - Provide a clear, descriptive title
   - Explain why this represents a gap in the research
   - Suggest a specific direction for future research to address this gap
4. Conclude with a brief paragraph on the overall implications of these gaps

Format each gap as:
## [Gap Title]
[2 sentences explaining the gap]
[1 sentence suggesting future research direction]

Query: {question}
"""
)

def process_pdf(pdf_path):
    """Process PDF and create vector database"""
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    return FAISS.from_documents(chunks, embeddings)

def query_rag(pdf_path, query_type):
    """Perform RAG query on the PDF"""
    vector_db = process_pdf(pdf_path)
    retriever = vector_db.as_retriever(search_kwargs={"k": 4})
    prompt = key_insights_prompt if query_type == "Key Insights" else research_gaps_prompt
    document_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | document_chain
    response = rag_chain.invoke(query_type)
    sources = "Analysis based on document contents"
    return response, sources

def ui_interface(pdf_file, query_type):
    """Handle UI interface for both Gradio and FastAPI"""
    if hasattr(pdf_file, 'name') and os.path.exists(pdf_file.name):
        # Regular file from FastAPI
        pdf_path = pdf_file.name
    else:
        # For Gradio in Jupyter, we need special handling
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            # Handle various file object types
            if isinstance(pdf_file, str) and os.path.exists(pdf_file):
                # If it's a path string
                with open(pdf_file, 'rb') as f:
                    temp_file.write(f.read())
            elif hasattr(pdf_file, 'read'):
                # If it's a file-like object
                content = pdf_file.read()
                if isinstance(content, str):
                    temp_file.write(content.encode('utf-8'))
                else:
                    temp_file.write(content)
            else:
                # Try direct conversion to bytes
                temp_file.write(pdf_file if isinstance(pdf_file, bytes) else str(pdf_file).encode('utf-8'))
            pdf_path = temp_file.name
    
    try:
        answer, sources = query_rag(pdf_path, query_type)
        return answer, sources
    finally:
        # Clean up temp file if we created one
        if pdf_path != getattr(pdf_file, 'name', '') and os.path.exists(pdf_path):
            os.remove(pdf_path)