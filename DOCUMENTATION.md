# Starbucks Procurement Multi-Agent System Documentation

## System Overview

The Starbucks Procurement Multi-Agent System is an AI-powered solution designed to automate and optimize the coffee bean procurement process for Starbucks. The system leverages multiple specialized autonomous agents that collaborate to handle the entire procurement lifecycle - from sourcing suppliers to negotiating contracts and managing orders.

## Core Objectives

1. **Automate Procurement Decisions**: Reduce manual intervention in routine procurement tasks
2. **Optimize Supply Chain**: Identify optimal suppliers based on quality, price, and sustainability
3. **Enhance Visibility**: Provide real-time insights into procurement activities
4. **Improve Decision-Making**: Leverage market data to make data-driven procurement decisions
5. **Ensure Sustainability**: Prioritize suppliers with strong sustainability practices

## System Architecture

The system is built on a modular architecture with the following components:

1. **Multi-Agent Framework**: Based on CrewAI, enabling agent collaboration
2. **Market Simulator**: Generates realistic market conditions and supplier data
3. **Agent API**: Provides endpoints for monitoring agent activities
4. **Dashboard**: Visualizes procurement activities and market data

### System Architecture Diagram

```
+----------------------------------------------+
|                                              |
|           STARBUCKS PROCUREMENT              |
|             MULTI-AGENT SYSTEM               |
|                                              |
+----------------------------------------------+
                      |
        +-------------+-------------+
        |             |             |
+-------v------+ +----v--------+ +-v------------+
|              | |             | |              |
|  Coffee Bean | | Contract    | | Order        |
|  Sourcing    | | Negotiation | | Management   |
|  Agent       | | Agent       | | Agent        |
|              | |             | |              |
+--------------+ +-------------+ +--------------+
        |             |             |
        +------+------+------+------+
               |             |
     +---------v-+      +----v-------+
     |           |      |            |
     | CrewAI    <----->  Agent API  |
     | Framework |      |            |
     |           |      +----+-------+
     +---------+-+           |
               |             |
     +---------v-+      +----v-------+
     |           |      |            |
     | Market    |      | Dashboard  |
     | Simulator |      |            |
     |           |      |            |
     +-----------+      +------------+
```

## Agent Roles and Responsibilities

### 1. Coffee Bean Sourcing Agent

**Primary Role**: Identifies and evaluates potential coffee bean suppliers worldwide.

**Responsibilities**:
- Analyze supplier quality scores and sustainability practices
- Evaluate supplier reliability and capacity
- Monitor supplier certifications (Organic, Fair Trade, Rainforest Alliance)
- Recommend optimal suppliers based on current needs

**Key Tools**:
- `get_all_suppliers`: Retrieves the complete list of available suppliers
- `evaluate_supplier_quality`: Assesses the quality of beans from specific suppliers
- `get_market_conditions`: Monitors current coffee market conditions to inform sourcing decisions

### 2. Contract Negotiation Agent

**Primary Role**: Handles supplier negotiations and contract management.

**Responsibilities**:
- Negotiate pricing and terms with selected suppliers
- Ensure contract compliance with Starbucks standards
- Manage contract renewals and amendments
- Optimize contract terms for cost efficiency

**Key Tools**:
- `get_active_contracts`: Retrieves all current active contracts
- `propose_contract`: Creates new contract proposals with suppliers
- `negotiate_contract`: Handles the negotiation process with suppliers
- `get_contract_details`: Retrieves detailed information about specific contracts
- `finalize_contract`: Completes the contract process and activates the contract

### 3. Order Management Agent

**Primary Role**: Manages the purchasing process and order tracking.

**Responsibilities**:
- Create purchase orders based on active contracts
- Track order status and delivery schedules
- Manage order modifications and cancellations
- Coordinate with other agents for procurement optimization

**Key Tools**:
- `get_active_orders`: Retrieves all current active purchase orders
- `get_order_details`: Gets detailed information about specific orders
- `create_order`: Creates new purchase orders based on contracts
- `track_order`: Monitors the status of orders in the supply chain
- `update_order_status`: Modifies the status of existing orders

### Inter-Agent Communication Tools

The agents can communicate and collaborate using:

- `Delegate work to coworker`: Assigns specific tasks to other agents
- `Ask question to coworker`: Requests information from other agents

## Workflow Process

The multi-agent workflow follows these steps:

1. **Initialization**:
   - System generates initial market data and supplier information
   - Agents are initialized with their specific tools and capabilities

2. **Market Simulation**:
   - Coffee market conditions are updated regularly (every 10 seconds)
   - Price fluctuations, regional variations, and market factors are simulated

3. **Agent Workflow Execution**:
   - Workflows run sequentially (one completes before the next begins)
   - Each workflow uses the market data at the moment it starts
   - Workflow execution takes approximately 5-10 minutes to complete

4. **Sourcing Phase**:
   - Coffee Bean Sourcing Agent evaluates all available suppliers
   - Analyzes quality scores, sustainability practices, and certifications
   - Recommends optimal suppliers based on current needs and market conditions

5. **Negotiation Phase**:
   - Contract Negotiation Agent proposes contracts with selected suppliers
   - Negotiates terms including price, volume, and delivery schedule
   - Ensures contracts meet all required criteria (payment terms, quality requirements)
   - Finalizes contracts when all conditions are met

6. **Order Management Phase**:
   - Order Management Agent creates purchase orders based on active contracts
   - Tracks order status and estimated delivery dates
   - Manages any issues with orders or deliveries

7. **Continuous Operation**:
   - System maintains persistent data between workflow runs
   - Orders and contracts accumulate over time
   - Agents adapt to changing market conditions

### Workflow Process Diagram

```
+-------------------+     +-------------------+     +-------------------+
|                   |     |                   |     |                   |
| MARKET SIMULATION |---->| AGENT WORKFLOW    |---->| SYSTEM STATE      |
| (Every 10 sec)    |     | EXECUTION         |     | UPDATES           |
|                   |     |                   |     |                   |
+-------------------+     +-------------------+     +-------------------+
                               |
                               | Sequential Execution
                               v
+-------------------+     +-------------------+     +-------------------+
|                   |     |                   |     |                   |
| SOURCING PHASE    |---->| NEGOTIATION PHASE |---->| ORDER MANAGEMENT  |
| Coffee Bean       |     | Contract          |     | PHASE             |
| Sourcing Agent    |     | Negotiation Agent |     | Order Agent       |
+-------------------+     +-------------------+     +-------------------+
        |                         |                         |
        v                         v                         v
+-------------------+     +-------------------+     +-------------------+
| • Evaluate        |     | • Propose         |     | • Create          |
|   suppliers       |     |   contracts       |     |   purchase orders |
| • Analyze quality |     | • Negotiate terms |     | • Track orders    |
| • Check           |     | • Finalize        |     | • Manage          |
|   sustainability  |     |   agreements      |     |   deliveries      |
+-------------------+     +-------------------+     +-------------------+
                               |
                               | Results Persist Between Runs
                               v
                     +-------------------+
                     |                   |
                     | DASHBOARD UPDATES |
                     | Real-time         |
                     | visualization     |
                     +-------------------+
```
## Technical Implementation

### Core Technologies

- **CrewAI**: Framework for managing agent collaboration
- **FastAPI**: Web framework for API endpoints and WebSocket connections
- **Dash/Streamlit**: Dashboard frameworks for visualization
- **OpenAI API**: Powers agent decision-making capabilities

### Key Files and Components

1. **agents/crew_manager.py**:
   - Manages the Starbucks Procurement Multi-Agent System
   - Initializes agents and their tools
   - Processes agent messages and system state
   - Handles agent collaboration and task execution

2. **agents/agent_definitions.py**:
   - Defines the three specialized agents
   - Configures agent parameters and capabilities
   - Sets agent goals and backstories

3. **agents/tools.py**:
   - Implements the specialized tools for each agent
   - Connects agent actions to the market simulator

4. **simulation/market_simulator.py**:
   - Simulates the coffee market conditions
   - Manages suppliers, contracts, and orders
   - Provides market data to the agents

5. **simulation/data_generator.py**:
   - Generates initial market data and supplier information
   - Creates realistic coffee market conditions
   - Randomizes supplier attributes and market factors

6. **agent_api.py**:
   - Provides API endpoints for monitoring agent activities
   - Allows external systems to trigger agent workflows
   - Returns agent messages and system state

7. **app.py**:
   - Main application entry point
   - Manages WebSocket connections for real-time updates
   - Coordinates market simulation and agent workflows
   - Serves the dashboard application

### Environment Configuration

The system requires:
- **OpenAI API Key**: Stored in `.env` file for agent decision-making
- **PYTHONIOENCODING**: Set to `utf-8` to handle special characters

## Data Flow

1. **Market Data Generation**:
   - System generates realistic market data and supplier information
   - Data includes prices, supplier details, and market conditions

2. **Agent Decision-Making**:
   - Agents receive current market data and system state
   - Each agent makes decisions based on their specialized knowledge
   - Decisions are communicated to other agents when needed

3. **System State Updates**:
   - Agent actions modify the system state (suppliers, contracts, orders)
   - State changes persist between workflow runs
   - System broadcasts updates to connected clients

### Data Flow Diagram

```
+------------------+
| Initial Data     |
| Generation       |
+--------+---------+
         |
         v
+--------+---------+     +------------------+
|                  |     |                  |
| Market Simulator +---->+ Market Data      |
|                  |     | (Updated every   |
+------------------+     |  10 seconds)     |
                         |                  |
                         +--------+---------+
                                  |
                                  v
+------------------+     +--------+---------+     +------------------+
|                  |     |                  |     |                  |
| System State     +<----+ Agent Workflow   +---->+ Agent Messages   |
| - Suppliers      |     | Execution        |     | - Actions        |
| - Contracts      |     | (Sequential      |     | - Decisions      |
| - Orders         |     |  processing)     |     | - Insights       |
+--------+---------+     +------------------+     +--------+---------+
         |                                                 |
         |                                                 |
         v                                                 v
+--------+---------+                             +---------+--------+
|                  |                             |                  |
| Dashboard        |                             | API Endpoints    |
| Visualization    |                             | - WebSockets     |
|                  |                             | - REST API       |
+------------------+                             +------------------+
```

## Performance Considerations

- **Workflow Duration**: Complete agent workflows take 5-10 minutes
- **Market Updates**: Market conditions update every 10 seconds
- **Sequential Execution**: Workflows run one at a time to prevent conflicts
- **Persistent State**: System maintains state between workflow runs

## Extensibility

The system is designed for extensibility:

1. **Adding New Agents**: Additional specialized agents can be created
2. **New Tools**: Agent capabilities can be extended with new tools
3. **Market Factors**: Additional market simulation factors can be added
4. **Integration Points**: System can connect to external data sources or systems

## Conclusion

The Starbucks Procurement Multi-Agent System demonstrates how autonomous AI agents can collaborate to manage complex business processes. By dividing responsibilities among specialized agents and enabling their collaboration, the system achieves more sophisticated decision-making than would be possible with a single agent approach.

This multi-agent architecture provides a scalable foundation for automating procurement decisions while maintaining the flexibility to adapt to changing market conditions and business requirements.
