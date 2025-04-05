import os
import sys
import subprocess
import time
from dotenv import load_dotenv

def check_requirements():
    """
    Check if all requirements are installed.
    """
    try:
        import crewai
        import fastapi
        import dash
        import plotly
        print("All required packages are installed.")
        return True
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return False

def check_api_key():
    """
    Check if the OpenAI API key is set.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("\nWARNING: OpenAI API key not found!")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here\n")
        
        # Create .env file from example if it doesn't exist
        if not os.path.exists(".env") and os.path.exists(".env.example"):
            print("Creating .env file from .env.example...")
            with open(".env.example", "r") as example_file:
                with open(".env", "w") as env_file:
                    env_file.write(example_file.read())
            print("Please edit the .env file and add your OpenAI API key.")
        
        return False
    
    return True

def setup_assets():
    """
    Set up static assets if they don't exist.
    """
    if not os.path.exists(os.path.join("dashboard", "static", "starbucks_logo.png")):
        print("Setting up static assets...")
        subprocess.run([sys.executable, "setup_assets.py"])

def run_application():
    """
    Run the Starbucks Procurement Multi-Agent System.
    """
    print("\nStarting Starbucks Procurement Multi-Agent System...\n")
    
    # Check requirements
    if not check_requirements():
        print("Please restart the application after installing requirements.")
        return
    
    # Check API key
    if not check_api_key():
        print("Please set your OpenAI API key and restart the application.")
        return
    
    # Set up assets
    setup_assets()
    
    # Run the application
    print("\nAll checks passed. Starting the application server...")
    print("\nDashboard will be available at: http://localhost:8000")
    print("Press Ctrl+C to stop the server.\n")
    
    subprocess.run([sys.executable, "app.py"])

if __name__ == "__main__":
    run_application()
