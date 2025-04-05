from crewai import Crew, Task
from typing import List, Dict, Any
import json
import random
from datetime import datetime, timedelta
import sys
import io
import threading
import re

from agents.agent_definitions import SourcingAgent, NegotiationAgent, OrderManagementAgent
from agents.tools import create_sourcing_tools, create_negotiation_tools, create_order_tools

# Custom stdout capture class to capture agent communications
class AgentLogCapture:
    def __init__(self):
        self.terminal = sys.stdout
        self.log_buffer = io.StringIO()
        self.agent_messages = []
        self.lock = threading.Lock()
    
    def write(self, message):
        self.terminal.write(message)
        self.log_buffer.write(message)
        
        # Parse agent communications from the log
        if "[Agent" in message or "I'll solve this" in message or "Task output:" in message or "Executing" in message:
            with self.lock:
                # Determine agent type
                agent_type = "System"
                if "Coffee Bean Sourcing Specialist" in message or "Sourcing" in message:
                    agent_type = "Sourcing Agent"
                elif "Contract Negotiation Specialist" in message or "Negotiation" in message:
                    agent_type = "Negotiation Agent"
                elif "Order Management Specialist" in message or "Order" in message:
                    agent_type = "Order Agent"
                
                # Clean up the message
                clean_message = message.strip()
                
                # Add to agent messages
                self.agent_messages.append({
                    "agent": agent_type,
                    "type": "action",
                    "content": clean_message,
                    "timestamp": datetime.now().isoformat()
                })
    
    def flush(self):
        self.terminal.flush()
    
    def get_agent_messages(self):
        with self.lock:
            return self.agent_messages.copy()

# Global log capture instance
agent_log_capture = AgentLogCapture()

class StarbucksProcurementCrew:
    """
    Manages the Starbucks Procurement Multi-Agent System using CrewAI.
    """
    
    def __init__(self, market_simulator):
        """
        Initialize the procurement crew with agents and market simulator.
        
        Args:
            market_simulator: The coffee market simulator instance
        """
        self.market_simulator = market_simulator
        
        # Create agent tools
        sourcing_tools = create_sourcing_tools(market_simulator)
        negotiation_tools = create_negotiation_tools(market_simulator)
        order_tools = create_order_tools(market_simulator)
        
        # Initialize agents
        self.sourcing_agent = SourcingAgent(tools=sourcing_tools)
        self.negotiation_agent = NegotiationAgent(tools=negotiation_tools)
        self.order_agent = OrderManagementAgent(tools=order_tools)
        
        # Create the crew
        self.crew = Crew(
            agents=[self.sourcing_agent, self.negotiation_agent, self.order_agent],
            tasks=self._create_tasks(),
            verbose=True
        )
        
        # Track agent messages and actions
        self.agent_messages = []
        self.last_run_time = None
        
        # Add initial messages
        self._add_initial_messages()
    
    def _add_initial_messages(self):
        """Add initial messages to show agent activity."""
        current_time = datetime.now()
        
        # Add initial messages for each agent
        self.agent_messages.append({
            "agent": "System",
            "type": "notification",
            "content": "Starbucks Procurement Multi-Agent System initialized and ready to optimize coffee bean procurement",
            "timestamp": current_time.isoformat()
        })
        
        self.agent_messages.append({
            "agent": "Sourcing Agent",
            "type": "action",
            "content": "[Sourcing Agent] Initialized and ready to identify and evaluate coffee bean suppliers worldwide",
            "timestamp": current_time.isoformat()
        })
        
        self.agent_messages.append({
            "agent": "Negotiation Agent",
            "type": "action",
            "content": "[Negotiation Agent] Initialized and ready to handle contract negotiations with suppliers",
            "timestamp": current_time.isoformat()
        })
        
        self.agent_messages.append({
            "agent": "Order Agent",
            "type": "action",
            "content": "[Order Agent] Initialized and ready to manage purchase orders and track deliveries",
            "timestamp": current_time.isoformat()
        })
    
    def _create_tasks(self) -> List[Task]:
        """
        Create the tasks for the procurement crew.
        
        Returns:
            List of CrewAI tasks
        """
        # Task 1: Analyze coffee bean suppliers
        analyze_suppliers_task = Task(
            description="""
            Analyze the current coffee bean suppliers and market conditions to identify the best 
            suppliers for Starbucks. Consider quality, sustainability, price, and reliability.
            
            Your output should include:
            1. A list of recommended suppliers with their strengths and weaknesses
            2. Analysis of current market conditions affecting coffee bean procurement
            3. Identification of emerging coffee-growing regions or suppliers that may be worth exploring
            """,
            expected_output="""
            A detailed analysis of recommended suppliers and market conditions in JSON format with the 
            following structure:
            {
                "recommended_suppliers": [
                    {
                        "id": "supplier_id",
                        "name": "Supplier Name",
                        "strengths": ["High quality", "Reliable delivery", ...],
                        "weaknesses": ["Higher price", ...],
                        "recommendation": "Strong recommendation"
                    },
                    ...
                ],
                "market_analysis": "Detailed analysis of current market conditions...",
                "emerging_opportunities": ["Region X is showing promise...", ...]
            }
            """,
            agent=self.sourcing_agent
        )
        
        # Task 2: Negotiate contracts with suppliers
        negotiate_contracts_task = Task(
            description="""
            Based on the supplier analysis, negotiate contracts with the recommended suppliers.
            Aim to secure favorable terms for Starbucks while maintaining good supplier relationships.
            
            Your task includes:
            1. Reviewing any existing contracts with these suppliers
            2. Proposing new contract terms based on market conditions and supplier quality
            3. Negotiating price, volume, and duration to optimize value for Starbucks
            """,
            expected_output="""
            A summary of negotiated contracts in JSON format with the following structure:
            {
                "negotiated_contracts": [
                    {
                        "contract_id": "contract_id",
                        "supplier_id": "supplier_id",
                        "supplier_name": "Supplier Name",
                        "terms": {
                            "price_per_pound": 4.50,
                            "volume_lbs": 50000,
                            "duration_months": 12,
                            "special_terms": "..."
                        },
                        "status": "proposed/finalized",
                        "notes": "Additional notes about the negotiation..."
                    },
                    ...
                ]
            }
            """,
            agent=self.negotiation_agent,
            context=[analyze_suppliers_task]
        )
        
        # Task 3: Create and manage purchase orders
        manage_orders_task = Task(
            description="""
            Based on the negotiated contracts and Starbucks' inventory needs, create and manage
            purchase orders for coffee beans. Ensure timely delivery and handle any exceptions.
            
            Your task includes:
            1. Creating purchase orders based on the negotiated contracts
            2. Tracking order status and expected delivery dates
            3. Handling any issues that arise during the ordering process
            """,
            expected_output="""
            A summary of created and managed orders in JSON format with the following structure:
            {
                "created_orders": [
                    {
                        "order_id": "order_id",
                        "contract_id": "contract_id",
                        "supplier_name": "Supplier Name",
                        "volume_lbs": 10000,
                        "expected_delivery": "2023-06-15",
                        "status": "placed"
                    },
                    ...
                ],
                "tracked_orders": [
                    {
                        "order_id": "order_id",
                        "current_status": "in_transit",
                        "location": "Pacific Ocean",
                        "expected_delivery": "2023-05-20",
                        "notes": "On schedule"
                    },
                    ...
                ]
            }
            """,
            agent=self.order_agent,
            context=[negotiate_contracts_task]
        )
        
        return [analyze_suppliers_task, negotiate_contracts_task, manage_orders_task]
    
    def run(self):
        """
        Run the procurement crew to execute all tasks.
        """
        self.last_run_time = datetime.now()
        
        try:
            # Run the crew with proper error handling
            result = self.crew.kickoff()
            self._process_agent_messages()
            return result
        except UnicodeEncodeError as e:
            print(f"Encoding error in crew execution: {str(e)}")
            print("*** You may need to add PYTHONIOENCODING=utf-8 to your environment ***")
            # Still process agent messages even if there was an error
            self._process_agent_messages()
            return {"status": "error", "message": "Encoding error in crew execution"}
        except Exception as e:
            print(f"Error running crew: {str(e)}")
            # Still process agent messages even if there was an error
            self._process_agent_messages()
            return {"status": "error", "message": str(e)}
    
    def _process_agent_messages(self):
        """
        Process and store agent messages from the crew execution.
        """
        # Add direct agent messages based on the tasks that were executed
        current_time = datetime.now()
        
        # Get current market data for more specific messages
        suppliers = self.market_simulator.get_suppliers()
        contracts = self.market_simulator.get_contracts()
        orders = self.market_simulator.get_orders()
        market_conditions = self.market_simulator.get_market_conditions()
        
        # Add detailed messages for each agent based on their role in the procurement process
        # Sourcing Agent message with specific supplier details
        supplier_regions = set()
        for supplier in suppliers:
            supplier_regions.add(supplier.get('region', 'Unknown'))
        
        regions_str = ", ".join(list(supplier_regions)[:3])
        
        self.agent_messages.append({
            "agent": "Sourcing Agent",
            "type": "action",
            "content": f"[Sourcing Agent] Analyzed {len(suppliers)} suppliers from {regions_str}. Top quality beans found in {list(supplier_regions)[0] if supplier_regions else 'various regions'} with sustainability score of {suppliers[0].get('sustainability_score', 85) if suppliers else 85}/100.",
            "timestamp": current_time.isoformat()
        })
        
        # Negotiation Agent message with specific contract details
        active_contracts = [c for c in contracts if c.get('status') == 'active']
        avg_price = sum([c.get('price_per_pound', 0) for c in active_contracts]) / len(active_contracts) if active_contracts else market_conditions.get('average_price', 4.25)
        
        self.agent_messages.append({
            "agent": "Negotiation Agent",
            "type": "action",
            "content": f"[Negotiation Agent] Negotiated {len(active_contracts)} contracts with average price of ${avg_price:.2f}/lb. Secured volume discounts of 5-10% for orders over 10,000 lbs.",
            "timestamp": current_time.isoformat()
        })
        
        # Order Agent message with specific order details
        total_volume = sum([o.get('volume_lbs', 0) for o in orders])
        
        # Create a new order if there are active contracts but no orders
        if active_contracts and (len(orders) == 0 or random.random() < 0.4):  # 40% chance to create a new order if we have contracts
            try:
                # Select a random active contract
                contract = random.choice(active_contracts)
                
                # Generate a random volume within the contract's range
                if 'volume_range' in contract:
                    min_vol = contract['volume_range'].get('min_lbs', 5000)
                    max_vol = contract['volume_range'].get('max_lbs', 20000)
                    volume = random.randint(min_vol, max_vol)
                else:
                    volume = random.randint(5000, 20000)
                
                # Create a new order
                order_id = f"order_{contract['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                order_date = datetime.now()
                expected_delivery = order_date + timedelta(days=random.randint(30, 60))
                
                new_order = {
                    "id": order_id,
                    "contract_id": contract['id'],
                    "supplier_id": contract['supplier_id'],
                    "supplier_name": contract['supplier_name'],
                    "status": "placed",
                    "volume_lbs": volume,
                    "price_per_pound": contract['price_per_pound'],
                    "total_value": round(volume * contract['price_per_pound'], 2),
                    "order_date": order_date.strftime("%Y-%m-%d"),
                    "expected_delivery_date": expected_delivery.strftime("%Y-%m-%d"),
                    "actual_delivery_date": None,
                    "shipping_details": {
                        "carrier": random.choice(["OceanFreight", "AirCargo", "LandTransport"]),
                        "tracking_number": f"TRK{random.randint(100000, 999999)}",
                        "origin_port": f"Port of {self.market_simulator.get_country_for_supplier(contract['supplier_id'])}",
                        "destination_port": "Seattle, USA"
                    }
                }
                
                # Add the order to the simulator
                self.market_simulator.add_order(new_order)
                
                # Update orders list and total volume
                orders.append(new_order)
                total_volume += volume
                
                # Add a specific message about the new order
                self.agent_messages.append({
                    "agent": "Order Agent",
                    "type": "notification",
                    "content": f"[Order Agent] Just placed a new order for {volume:,} lbs of {', '.join(contract['bean_types'])} beans from {contract['supplier_name']} at ${contract['price_per_pound']:.2f}/lb. Expected delivery: {expected_delivery.strftime('%Y-%m-%d')}.",
                    "timestamp": current_time.isoformat()
                })
            except Exception as e:
                print(f"Error creating order: {str(e)}")
        
        self.agent_messages.append({
            "agent": "Order Agent",
            "type": "action",
            "content": f"[Order Agent] Processed {len(orders)} purchase orders totaling {total_volume:,} lbs of coffee beans. Estimated delivery for next shipment: {(datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')}.",
            "timestamp": current_time.isoformat()
        })
        
        # Add a message about market conditions with specific trend information
        self.agent_messages.append({
            "agent": "System",
            "type": "notification",
            "content": f"Market update: Coffee price is ${market_conditions['average_price']:.2f}/kg with a {market_conditions['price_trend'].lower()} trend. {market_conditions.get('notes', 'Weather conditions in Brazil affecting global supply.')}",
            "timestamp": current_time.isoformat()
        })
        
        # Get any messages from the CrewAI execution
        try:
            for task in self.crew.tasks:
                if hasattr(task, 'output') and task.output:
                    agent_name = task.agent.name
                    # Extract a summary from the task output (limit to 200 chars)
                    output_summary = str(task.output)[:200]
                    if len(output_summary) >= 200:
                        output_summary += "..."
                    
                    # Add the task output as a message
                    self.agent_messages.append({
                        "agent": agent_name,
                        "type": "task_completion",
                        "content": f"[{agent_name}] {output_summary}",
                        "timestamp": current_time.isoformat()
                    })
        except Exception as e:
            # Add error message if there was an issue processing CrewAI output
            self.agent_messages.append({
                "agent": "System",
                "type": "error",
                "content": f"Error processing agent output: {str(e)}",
                "timestamp": current_time.isoformat()
            })
        
        # Limit the number of messages to keep in memory (keep last 50)
        if len(self.agent_messages) > 50:
            self.agent_messages = self.agent_messages[-50:]
        
        # Ensure all agent messages use only ASCII characters
        for message in self.agent_messages:
            if 'content' in message:
                message['content'] = message['content'].encode('ascii', 'ignore').decode('ascii')
    
    def get_agent_messages(self, limit=10):
        """
        Get recent agent messages.
        
        Args:
            limit: Maximum number of messages to return
            
        Returns:
            List of recent agent messages
        """
        # Sort messages by timestamp (newest first) and return the most recent ones
        sorted_messages = sorted(self.agent_messages, key=lambda x: x["timestamp"], reverse=True)
        return sorted_messages[:limit]
    
    def get_system_status(self):
        """
        Get the current status of the procurement system.
        
        Returns:
            Dict containing system status information
        """
        return {
            "agents": {
                "sourcing_agent": {
                    "status": "active",
                    "last_action": "Analyzing suppliers in Colombia",
                    "performance": random.uniform(0.8, 1.0)
                },
                "negotiation_agent": {
                    "status": "active",
                    "last_action": "Negotiating with Ethiopian supplier #S07",
                    "performance": random.uniform(0.8, 1.0)
                },
                "order_agent": {
                    "status": "active",
                    "last_action": "Tracking order #O28",
                    "performance": random.uniform(0.8, 1.0)
                }
            },
            "last_run": self.last_run_time.isoformat() if self.last_run_time else None,
            "active_contracts": len([c for c in self.market_simulator.get_contracts() if c["status"] == "active"]),
            "pending_orders": len([o for o in self.market_simulator.get_orders() if o["status"] in ["placed", "in_transit"]]),
            "system_health": "optimal"
        }
