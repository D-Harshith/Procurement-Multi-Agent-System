"""
Dashboard for Starbucks Procurement Multi-Agent System

This script provides a web dashboard to visualize agent activities and system state.
"""

import os
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import requests
import asyncio
from typing import List

# Initialize FastAPI app
app = FastAPI(title="Starbucks Procurement Dashboard")

# Mount static files
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="dashboard/templates")

# API URL
API_URL = "http://localhost:8081"

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Dashboard routes
@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """Render the dashboard page."""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Get data from API
            try:
                # Get agents
                agents_response = requests.get(f"{API_URL}/agents")
                agents_data = agents_response.json()
                
                # Get suppliers
                suppliers_response = requests.get(f"{API_URL}/suppliers")
                suppliers_data = suppliers_response.json()
                
                # Get contracts
                contracts_response = requests.get(f"{API_URL}/contracts")
                contracts_data = contracts_response.json()
                
                # Get orders
                orders_response = requests.get(f"{API_URL}/orders")
                orders_data = orders_response.json()
                
                # Get market conditions
                market_response = requests.get(f"{API_URL}/market")
                market_data = market_response.json()
                
                # Get messages
                messages_response = requests.get(f"{API_URL}/messages")
                messages_data = messages_response.json()
                
                # Combine all data
                dashboard_data = {
                    "agents": agents_data.get("agents", []),
                    "suppliers": suppliers_data.get("suppliers", []),
                    "contracts": contracts_data.get("contracts", []),
                    "orders": orders_data.get("orders", []),
                    "market_conditions": market_data.get("market_conditions", {}),
                    "messages": messages_data.get("messages", [])
                }
                
                # Send data to client
                await websocket.send_text(json.dumps(dashboard_data))
                
            except Exception as e:
                print(f"Error fetching data: {str(e)}")
                await websocket.send_text(json.dumps({"error": str(e)}))
            
            # Wait for 5 seconds before the next update
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/run_agents")
async def run_agents():
    """Run the agent system once and broadcast the results."""
    try:
        response = requests.post(f"{API_URL}/run_agents")
        data = response.json()
        
        # Broadcast update notification
        await manager.broadcast(json.dumps({"action": "agents_run", "status": data.get("status")}))
        
        return data
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Run the server if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("dashboard_app:app", host="0.0.0.0", port=8082, reload=False)
