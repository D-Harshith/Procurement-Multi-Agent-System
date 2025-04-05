# Starbucks Procurement Multi-Agent System

A multi-agent system for Starbucks supply chain procurement management using CrewAI.

## Overview

This system simulates a coffee bean procurement process for Starbucks with three specialized agents:

1. **Coffee Bean Sourcing Agent**: Identifies and evaluates potential coffee bean suppliers worldwide
2. **Contract Negotiation Agent**: Handles supplier negotiations and contract management
3. **Order Management Agent**: Manages the purchasing process and order tracking

## Features

- Autonomous agent decision-making
- Inter-agent communication and coordination
- Simulated coffee market environment
- Web dashboard for visualization
- Real-time agent activity monitoring

## Getting Started

### Prerequisites

- Python 3.9+
- OpenAI API key (for CrewAI agents)

### Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Running the Application

1. Start the web server:
   ```
   python app.py
   ```
2. Open your browser and navigate to `http://localhost:8000`

## System Architecture

- **Backend**: FastAPI, CrewAI
- **Frontend**: Dash, Plotly
- **Data Storage**: In-memory (simulated)
- **Agent Framework**: CrewAI

## Dashboard Components

- Global Sourcing Map
- Supplier Relationship Panel
- Order Status Board
- Agent Activity Log
- Market Intelligence Center
