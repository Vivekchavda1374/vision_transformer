#!/usr/bin/env python3
"""
Simple script to start the Vision Transformer Flask server
"""

import subprocess
import sys
import os
import webbrowser
import time
from threading import Timer

def open_browser():
    """Open browser after a delay"""
    webbrowser.open('http://localhost:5000')

def main():
    print("🚀 Starting Vision Transformer Web Application")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Please run this script from the genai directory.")
        sys.exit(1)
    
    print("📍 Server will be available at: http://localhost:5000")
    print("🔧 Using JAX with CPU backend")
    print("🤖 Vision Transformer model ready")
    print("=" * 50)
    
    # Open browser after 2 seconds
    Timer(2.0, open_browser).start()
    
    try:
        # Start Flask app
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()