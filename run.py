#!/usr/bin/env python3
"""
Entrypoint script for the Research Paper Analyzer.
Run this file to start the application.
"""

import nest_asyncio
import webbrowser
import time
import threading
from app.main import run_server

if __name__ == "__main__":
    # Apply nest_asyncio to allow nested event loops in Jupyter
    nest_asyncio.apply()
    
    # Start the server in a background thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Give the server a moment to start
    time.sleep(2)
    
    # Open the app in a browser
    webbrowser.open('http://127.0.0.1:8000')
    
    print("Server is running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server shutting down...")