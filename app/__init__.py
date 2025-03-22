"""
Research Paper Analyzer
-----------------------

A web application that uses Retrieval-Augmented Generation (RAG) to analyze 
research papers and extract key insights or identify research gaps.
"""

__version__ = "0.1.0"
__author__ = "Dharshan"

# Import important functions to make them available at package level
from app.utils import query_rag, process_pdf
from app.main import app, run_server

# This allows users to import directly from the package
# Example: from app import query_rag