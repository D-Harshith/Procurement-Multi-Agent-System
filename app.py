import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from datetime import datetime, timedelta
import threading
import time
import random
import requests
from starlette.middleware.wsgi import WSGIMiddleware

# Import our agent system
from agents.crew_manager import StarbucksProcurementCrew
from simulation.market_simulator import CoffeeMarketSimulator
from simulation.data_generator import generate_initial_data
from dashboard.dash_app import create_dash_app

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Starbucks Procurement Multi-Agent System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

# Initialize our data
initial_data = generate_initial_data()
market_simulator = CoffeeMarketSimulator(initial_data)
procurement_crew = StarbucksProcurementCrew(market_simulator)

# Store connected WebSocket clients
connected_clients = set()

# Create a lock for thread-safe operations
data_lock = threading.Lock()

# Agent system state
system_state = {
    "suppliers": initial_data["suppliers"],
    "contracts": initial_data["contracts"],
    "orders": initial_data["orders"],
    "market_conditions": initial_data["market_conditions"],
    "agent_messages": procurement_crew.get_agent_messages(),  # Initialize with actual agent messages
    "system_status": procurement_crew.get_system_status(),
    "last_update": datetime.now().isoformat()
}

# Create the Dash app
dash_app = create_dash_app(system_state)

# Mount the Dash app as a WSGI application
app.mount("/", WSGIMiddleware(dash_app.server))

# Function to fetch agent messages from the agent API
def fetch_agent_messages():
    """Fetch agent messages from the agent API."""
    try:
        response = requests.get("http://localhost:8081/messages")
        if response.status_code == 200:
            return response.json().get("messages", [])
        return []
    except Exception as e:
        print(f"Error fetching agent messages: {str(e)}")
        return []

@app.get("/api/state")
async def get_state():
    """Get the current system state."""
    with data_lock:
        return system_state

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(1)  # Keep connection alive
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast_update(update):
    """Broadcast updates to all connected clients."""
    disconnected_clients = set()
    for client in connected_clients:
        try:
            await client.send_json(update)
        except Exception:
            disconnected_clients.add(client)
    
    # Remove disconnected clients
    connected_clients.difference_update(disconnected_clients)

async def run_agent_system():
    """Background task to run the agent system."""
    global system_state
    
    # Initial delay to allow the server to start
    await asyncio.sleep(2)
    
    # Flag to track if agents are currently running
    agents_running = False
    
    # Initial update with existing messages
    with data_lock:
        system_state = {
            "suppliers": market_simulator.get_suppliers(),
            "contracts": market_simulator.get_contracts(),
            "orders": market_simulator.get_orders(),
            "market_conditions": market_simulator.get_market_conditions(),
            "agent_messages": procurement_crew.get_agent_messages(),
            "system_status": procurement_crew.get_system_status(),
            "last_update": datetime.now().isoformat()
        }
    
    # Broadcast initial state
    await broadcast_update({
        "type": "state_update",
        "data": system_state
    })
    
    while True:
        try:
            # Simulate market changes
            market_simulator.simulate_step()
            
            # Update market data in system state
            with data_lock:
                system_state["market_conditions"] = market_simulator.get_market_conditions()
                system_state["last_update"] = datetime.now().isoformat()
            
            # Broadcast market update to connected clients
            await broadcast_update({
                "type": "state_update",
                "data": system_state
            })
            
            # Only start a new agent workflow if previous one has finished
            if not agents_running:
                # Set flag to indicate agents are running
                agents_running = True
                
                # Run the agent system in a separate thread
                async def run_agents():
                    nonlocal agents_running
                    try:
                        # Run the procurement crew to generate agent messages
                        with data_lock:
                            # Run the procurement crew
                            result = procurement_crew.run()
                            
                            # Update system state with the latest agent messages
                            system_state.update({
                                "suppliers": market_simulator.get_suppliers(),
                                "contracts": market_simulator.get_contracts(),
                                "orders": market_simulator.get_orders(),
                                "agent_messages": procurement_crew.get_agent_messages(),
                                "system_status": procurement_crew.get_system_status(),
                                "last_update": datetime.now().isoformat()
                            })
                        
                        # Broadcast update to connected clients
                        await broadcast_update({
                            "type": "state_update",
                            "data": system_state
                        })
                        
                        # Print confirmation that agent messages were updated
                        print(f"Updated agent messages: {len(procurement_crew.get_agent_messages())} messages")
                        
                    except Exception as e:
                        print(f"Error running agent system: {str(e)}")
                    finally:
                        # Reset flag to indicate agents are no longer running
                        agents_running = False
                
                # Start agent workflow asynchronously
                asyncio.create_task(run_agents())
        
        except Exception as e:
            print(f"Error in agent system loop: {str(e)}")
        
        # Wait before next market update
        await asyncio.sleep(10)  # Update market data every 10 seconds

@app.on_event("startup")
async def startup_event():
    """Start the background task when the app starts."""
    asyncio.create_task(run_agent_system())

# Run the server if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8082, reload=False)
