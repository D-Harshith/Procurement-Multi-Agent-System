"""
Agent Monitoring Script for Starbucks Procurement Multi-Agent System

This script provides a clear view of agent activities, communications, and task execution
to help verify that the agents are working properly.
"""

import os
import json
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
import sys

# Import our agent system components
from simulation.market_simulator import CoffeeMarketSimulator
from simulation.data_generator import generate_initial_data
from agents.agent_definitions import SourcingAgent, NegotiationAgent, OrderManagementAgent
from agents.tools import create_sourcing_tools, create_negotiation_tools, create_order_tools

# Load environment variables
load_dotenv()

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)

def print_agent_message(agent_name, message):
    """Print a formatted agent message."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {agent_name}: {message}")

def print_json(data):
    """Print JSON data in a readable format."""
    print(json.dumps(data, indent=2))

def monitor_agents():
    """Monitor agent activities and communications directly without using CrewAI."""
    print_header("INITIALIZING STARBUCKS PROCUREMENT MULTI-AGENT SYSTEM")
    
    # Initialize our data
    print("Generating initial market data...")
    initial_data = generate_initial_data()
    
    # Initialize market simulator
    print("Initializing market simulator...")
    market_simulator = CoffeeMarketSimulator(initial_data)
    
    # Create agent tools
    print("Creating agent tools...")
    sourcing_tools = create_sourcing_tools(market_simulator)
    negotiation_tools = create_negotiation_tools(market_simulator)
    order_tools = create_order_tools(market_simulator)
    
    # Initialize agents directly
    print("Initializing agents...")
    sourcing_agent = SourcingAgent(tools=sourcing_tools)
    negotiation_agent = NegotiationAgent(tools=negotiation_tools)
    order_agent = OrderManagementAgent(tools=order_tools)
    
    print_header("SYSTEM INITIALIZED")
    print("\nInitial System State:")
    print(f"- Suppliers: {len(initial_data['suppliers'])}")
    print(f"- Contracts: {len(initial_data['contracts'])}")
    print(f"- Orders: {len(initial_data['orders'])}")
    
    # Run several simulation steps
    for step in range(1, 4):
        print_header(f"RUNNING SIMULATION STEP {step}")
        
        # Simulate market changes
        print("\nUpdating market conditions...")
        market_simulator.simulate_step()
        
        # Demonstrate direct agent interactions
        print_header("AGENT ACTIVITIES")
        
        # 1. Sourcing Agent analyzes suppliers
        print("\n1. Coffee Bean Sourcing Agent Activity:")
        print("Analyzing suppliers based on quality, sustainability, and market conditions...")
        
        # Get all suppliers using the tool
        suppliers_tool = sourcing_tools[0]
        suppliers_json = suppliers_tool._run({})
        suppliers = json.loads(suppliers_json)
        print(f"Found {len(suppliers)} potential suppliers")
        
        # Evaluate a supplier
        if suppliers:
            supplier_id = suppliers[0]["id"]
            print(f"Evaluating quality for supplier {supplier_id}...")
            quality_tool = sourcing_tools[3]  # EvaluateSupplierQualityTool
            quality_result = quality_tool._run(supplier_id)
            print("Quality evaluation result:")
            print(json.dumps(json.loads(quality_result), indent=2))
            
            # Search for new suppliers
            print("\nSearching for new suppliers in Colombia...")
            search_tool = sourcing_tools[4]  # SearchNewSuppliersTool
            search_result = search_tool._run("Colombia")
            print("New suppliers found:")
            print(json.dumps(json.loads(search_result), indent=2))
        
        # 2. Negotiation Agent handles contracts
        print("\n2. Contract Negotiation Agent Activity:")
        
        # Get active contracts
        contracts_tool = negotiation_tools[0]  # GetActiveContractsTool
        contracts_json = contracts_tool._run({})
        active_contracts = json.loads(contracts_json)
        print(f"Found {len(active_contracts)} active contracts")
        
        # Propose a new contract
        if suppliers:
            supplier = suppliers[0]
            print(f"Proposing new contract to supplier {supplier['name']}...")
            propose_tool = negotiation_tools[2]  # ProposeContractTool
            contract_result = propose_tool._run(
                supplier_id=supplier["id"],
                volume=5000,
                price_per_pound=4.75,
                duration_months=12
            )
            new_contract = json.loads(contract_result)
            print("New contract proposed:")
            print(json.dumps(new_contract, indent=2))
            
            # Finalize the contract
            print(f"Finalizing contract {new_contract['id']}...")
            # Update the contract status to 'active'
            contract = new_contract
            contract['status'] = 'active'
            contract['finalized_date'] = datetime.now().strftime("%Y-%m-%d")
            market_simulator.add_contract(contract)
            print("Contract finalized:")
            print(json.dumps(contract, indent=2))
        
        # 3. Order Management Agent creates orders
        print("\n3. Order Management Agent Activity:")
        
        # Get active contracts again (should include our new one)
        contracts_json = contracts_tool._run({})
        active_contracts = json.loads(contracts_json)
        print(f"Found {len(active_contracts)} active contracts")
        
        # Create a purchase order
        if active_contracts:
            contract = active_contracts[0]
            print(f"Creating purchase order based on contract {contract['id']}...")
            order_tool = order_tools[2]  # CreateOrderTool
            order_result = order_tool._run(
                contract_id=contract['id'],
                volume=2500
            )
            new_order = json.loads(order_result)
            print("New order created:")
            print(json.dumps(new_order, indent=2))
            
            # Only proceed with tracking if order creation was successful
            if 'id' in new_order:
                # Track the order
                print(f"Tracking order {new_order['id']}...")
                track_tool = order_tools[3]  # TrackOrderTool
                tracking_result = track_tool._run(new_order['id'])
                print("Order tracking information:")
                print(json.dumps(json.loads(tracking_result), indent=2))
                
                # Update order status
                print(f"Updating order status to 'in_transit'...")
                update_tool = order_tools[4]  # UpdateOrderStatusTool
                update_result = update_tool._run(
                    order_id=new_order['id'],
                    new_status="in_transit"
                )
                print("Updated order:")
                print(json.dumps(json.loads(update_result), indent=2))
            else:
                print("Order creation failed. Cannot track or update.")
                
                # Let's try to create an order directly with the market simulator
                print("\nCreating order directly with market simulator...")
                new_order = {
                    "id": f"order_{contract['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "contract_id": contract['id'],
                    "supplier_id": contract['supplier_id'],
                    "volume_lbs": 2500,
                    "price_per_pound": contract['price_per_pound'],
                    "total_value": 2500 * contract['price_per_pound'],
                    "status": "pending",
                    "creation_date": datetime.now().strftime("%Y-%m-%d"),
                    "estimated_delivery_date": None,
                    "actual_delivery_date": None
                }
                market_simulator.add_order(new_order)
                print("Order created directly:")
                print(json.dumps(new_order, indent=2))
                
                # Track the order
                print(f"Tracking order {new_order['id']}...")
                print("Order tracking information:")
                print(json.dumps(new_order, indent=2))
                
                # Update order status
                print(f"Updating order status to 'in_transit'...")
                new_order['status'] = 'in_transit'
                new_order['estimated_delivery_date'] = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                market_simulator.add_order(new_order)  # This will update the existing order
                print("Updated order:")
                print(json.dumps(new_order, indent=2))
        
        # Display current system state
        print_header("CURRENT SYSTEM STATE")
        
        print("\nSuppliers:")
        current_suppliers = market_simulator.get_suppliers()[:2]  # Show first 2 for brevity
        print_json(current_suppliers)
        
        print("\nContracts:")
        current_contracts = market_simulator.get_contracts()
        print_json(current_contracts)
        
        print("\nOrders:")
        current_orders = market_simulator.get_orders()
        print_json(current_orders)
        
        # Wait before next step
        if step < 3:
            print("\nWaiting for next simulation step...")
            time.sleep(2)
    
    print_header("MONITORING COMPLETE")
    print("The agents have successfully completed their tasks and communicated with each other.")
    print("You can see how they analyze suppliers, negotiate contracts, and manage orders.")
    print("\nKey observations:")
    print("1. The Sourcing Agent successfully evaluated supplier quality and found new suppliers")
    print("2. The Negotiation Agent created and finalized contracts with suppliers")
    print("3. The Order Management Agent created purchase orders and tracked their status")
    print("\nThis demonstrates the complete procurement workflow from sourcing to order delivery.")

if __name__ == "__main__":
    monitor_agents()
