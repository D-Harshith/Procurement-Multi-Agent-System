import os
import requests
import shutil
from pathlib import Path

def download_file(url, destination):
    """
    Download a file from a URL to a destination path.
    
    Args:
        url: URL to download from
        destination: Path to save the file to
    """
    print(f"Downloading {url} to {destination}...")
    
    # Create parent directories if they don't exist
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    # Download the file
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        print(f"Downloaded {destination}")
    else:
        print(f"Failed to download {url}: {response.status_code}")

def create_architecture_diagram():
    """
    Create a simple architecture diagram using ASCII art.
    """
    diagram = """
    +-----------------------+     +------------------------+     +------------------------+
    |                       |     |                        |     |                        |
    | Coffee Bean Sourcing  |     | Contract Negotiation   |     | Order Management       |
    | Agent                 |     | Agent                  |     | Agent                  |
    |                       |     |                        |     |                        |
    +-----------+-----------+     +------------+-----------+     +------------+-----------+
                |                              |                              |
                |                              |                              |
                v                              v                              v
    +-----------------------------------------------------------------------------------+
    |                                                                                   |
    |                          Message Broker / Event Bus                               |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
                |                              |                              |
                |                              |                              |
                v                              v                              v
    +-----------------------------------------------------------------------------------+
    |                                                                                   |
    |                          Shared State / Database                                  |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
                                             |
                                             |
                                             v
    +-----------------------------------------------------------------------------------+
    |                                                                                   |
    |                               Web Dashboard                                       |
    |                                                                                   |
    +-----------------------------------------------------------------------------------+
    """
    
    # Save the diagram as a text file
    diagram_path = os.path.join("dashboard", "static", "architecture.txt")
    os.makedirs(os.path.dirname(diagram_path), exist_ok=True)
    
    with open(diagram_path, "w") as f:
        f.write(diagram)
    
    print(f"Created architecture diagram at {diagram_path}")

def setup_assets():
    """
    Download and set up all necessary static assets for the application.
    """
    # Define the assets to download
    assets = [
        {
            "url": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Starbucks_Corporation_Logo_2011.svg/1200px-Starbucks_Corporation_Logo_2011.svg.png",
            "destination": os.path.join("dashboard", "static", "starbucks_logo.png")
        }
    ]
    
    # Download each asset
    for asset in assets:
        download_file(asset["url"], asset["destination"])
    
    # Create the architecture diagram
    create_architecture_diagram()
    
    print("Asset setup complete!")

if __name__ == "__main__":
    setup_assets()
