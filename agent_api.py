"""
Agent API for Starbucks Procurement Multi-Agent System

This script provides a simple API to monitor agent activities and system state.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import uvicorn
import json
from datetime import datetime

# Import our agent system
from agents.crew_manager import StarbucksProcurementCrew
from simulation.market_simulator import CoffeeMarketSimulator
from simulation.data_generator import generate_initial_data

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Starbucks Procurement Agent API")

# Initialize our data
initial_data = generate_initial_data()
market_simulator = CoffeeMarketSimulator(initial_data)
procurement_crew = StarbucksProcurementCrew(market_simulator)

# Run the crew once to initialize
try:
    procurement_crew.run()
except Exception as e:
    print(f"Initial crew run error (this is expected): {str(e)}")

# Agent messages storage
agent_messages = []

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Starbucks Procurement Agent API",
        "description": "API to monitor agent activities and system state",
        "endpoints": [
            {"path": "/", "description": "This information"},
            {"path": "/agents", "description": "Get information about all agents"},
            {"path": "/suppliers", "description": "Get all suppliers"},
            {"path": "/contracts", "description": "Get all contracts"},
            {"path": "/orders", "description": "Get all orders"},
            {"path": "/market", "description": "Get market conditions"},
            {"path": "/messages", "description": "Get agent messages"},
            {"path": "/run_agents", "description": "Run the agent system once"}
        ]
    }

@app.get("/agents")
async def get_agents():
    """Get information about all agents."""
    system_status = procurement_crew.get_system_status()
    return {"agents": system_status["agents"]}

@app.get("/suppliers")
async def get_suppliers():
    """Get all suppliers."""
    return {"suppliers": market_simulator.get_suppliers()}

@app.get("/contracts")
async def get_contracts():
    """Get all contracts."""
    return {"contracts": market_simulator.get_contracts()}

@app.get("/orders")
async def get_orders():
    """Get all orders."""
    return {"orders": market_simulator.get_orders()}

@app.get("/market")
async def get_market():
    """Get market conditions."""
    return {"market_conditions": market_simulator.get_market_conditions()}

@app.get("/messages")
async def get_messages():
    """
    Get all agent messages.
    """
    return {"messages": agent_messages}

@app.post("/messages")
async def add_message(message: dict):
    """
    Add a new agent message.
    """
    message["timestamp"] = datetime.now().isoformat()
    agent_messages.append(message)
    
    # Keep only the last 20 messages
    if len(agent_messages) > 20:
        agent_messages.pop(0)
    
    return {"status": "success", "message": "Message added"}

@app.post("/run_agents")
async def run_agents():
    """
    Run the multi-agent system.
    """
    try:
        # Simulate market changes
        market_simulator.simulate_step()
        
        # Run the procurement crew to generate real agent messages
        result = procurement_crew.run()
        
        # Get the actual agent messages from the procurement crew
        crew_messages = procurement_crew.get_agent_messages()
        
        # Update the agent_messages list with the actual messages from the crew
        for message in crew_messages:
            # Only add messages that aren't already in the list
            if message not in agent_messages:
                agent_messages.append(message)
        
        # Keep only the last 50 messages
        while len(agent_messages) > 50:
            agent_messages.pop(0)
        
        return {
            "status": "success", 
            "result": "Agents executed successfully",
            "message_count": len(agent_messages)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Run the server if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("agent_api:app", host="0.0.0.0", port=8081, reload=False)
