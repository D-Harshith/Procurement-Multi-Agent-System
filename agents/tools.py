from crewai.tools import BaseTool
from typing import List, Dict, Any, Optional
import json
import random
from datetime import datetime, timedelta

def create_sourcing_tools(market_simulator) -> List[BaseTool]:
    """
    Create tools for the Coffee Bean Sourcing Agent.
    
    Args:
        market_simulator: The coffee market simulator instance
        
    Returns:
        List of tools for the sourcing agent
    """
    
    class GetAllSuppliersTool(BaseTool):
        name: str = "get_all_suppliers"
        description: str = "Get information about all available coffee suppliers."
        
        def _run(self, args: Optional[Dict] = None) -> str:
            suppliers = market_simulator.get_suppliers()
            return json.dumps(suppliers, indent=2)
    
    class GetSupplierDetailsTool(BaseTool):
        name: str = "get_supplier_details"
        description: str = "Get detailed information about a specific supplier."
        
        def _run(self, supplier_id: str) -> str:
            suppliers = market_simulator.get_suppliers()
            supplier = next((s for s in suppliers if s['id'] == supplier_id), None)
            if supplier:
                return json.dumps(supplier, indent=2)
            return json.dumps({"error": f"Supplier with ID {supplier_id} not found"})
    
    class GetMarketConditionsTool(BaseTool):
        name: str = "get_market_conditions"
        description: str = "Get current coffee market conditions and trends."
        
        def _run(self, args: Optional[Dict] = None) -> str:
            market_conditions = market_simulator.get_market_conditions()
            return json.dumps(market_conditions, indent=2)
    
    class EvaluateSupplierQualityTool(BaseTool):
        name: str = "evaluate_supplier_quality"
        description: str = "Evaluate the quality of a supplier's coffee beans."
        
        def _run(self, supplier_id: str) -> str:
            suppliers = market_simulator.get_suppliers()
            supplier = next((s for s in suppliers if s['id'] == supplier_id), None)
            
            if not supplier:
                return json.dumps({"error": f"Supplier with ID {supplier_id} not found"})
            
            # Simulate quality evaluation
            quality_score = supplier.get('quality_score', random.uniform(60, 98))
            tasting_notes = supplier.get('tasting_notes', ['Unknown'])
            
            evaluation = {
                "supplier_id": supplier_id,
                "supplier_name": supplier.get('name', 'Unknown'),
                "quality_score": quality_score,
                "tasting_notes": tasting_notes,
                "evaluation_date": datetime.now().strftime("%Y-%m-%d"),
                "recommendation": "Recommended" if quality_score >= 80 else "Not Recommended",
                "detailed_analysis": f"The coffee beans from {supplier.get('name', 'this supplier')} "
                                    f"have a quality score of {quality_score:.1f}/100. "
                                    f"The beans exhibit notes of {', '.join(tasting_notes)}. "
                                    f"{'The quality is excellent and meets Starbucks standards.' if quality_score >= 80 else 'The quality does not meet Starbucks standards.'}"
            }
            
            return json.dumps(evaluation, indent=2)
    
    class SearchNewSuppliersTool(BaseTool):
        name: str = "search_new_suppliers"
        description: str = "Search for new potential coffee bean suppliers in a specific region."
        
        def _run(self, region: str) -> str:
            # Simulate finding new suppliers in the specified region
            new_suppliers = []
            
            # Generate 1-3 new potential suppliers
            for i in range(random.randint(1, 3)):
                supplier_id = f"new_{region.lower().replace(' ', '_')}_{i+1}"
                quality_score = random.uniform(70, 95)
                
                # Generate random tasting notes
                tasting_notes = []
                all_notes = ["chocolate", "nutty", "fruity", "floral", "citrus", "caramel", "spicy", "earthy", "berry", "vanilla"]
                for _ in range(random.randint(2, 4)):
                    note = random.choice(all_notes)
                    if note not in tasting_notes:
                        tasting_notes.append(note)
                
                new_supplier = {
                    "id": supplier_id,
                    "name": f"{region} Coffee Cooperative {i+1}",
                    "region": region,
                    "country": market_simulator.get_country_for_region(region),
                    "quality_score": quality_score,
                    "tasting_notes": tasting_notes,
                    "sustainability_rating": random.randint(3, 5),
                    "price_per_pound": round(random.uniform(3.0, 8.0), 2),
                    "minimum_order_quantity": random.randint(1000, 5000),
                    "lead_time_days": random.randint(30, 90),
                    "discovery_date": datetime.now().strftime("%Y-%m-%d")
                }
                
                new_suppliers.append(new_supplier)
            
            return json.dumps(new_suppliers, indent=2)
    
    return [
        GetAllSuppliersTool(),
        GetSupplierDetailsTool(),
        GetMarketConditionsTool(),
        EvaluateSupplierQualityTool(),
        SearchNewSuppliersTool()
    ]

def create_negotiation_tools(market_simulator) -> List[BaseTool]:
    """
    Create tools for the Contract Negotiation Agent.
    
    Args:
        market_simulator: The coffee market simulator instance
        
    Returns:
        List of tools for the negotiation agent
    """
    
    class GetActiveContractsTool(BaseTool):
        name: str = "get_active_contracts"
        description: str = "Get all active contracts with suppliers."
        
        def _run(self, args: Optional[Dict] = None) -> str:
            contracts = market_simulator.get_contracts()
            active_contracts = [c for c in contracts if c['status'] == 'active']
            return json.dumps(active_contracts, indent=2)
    
    class GetContractDetailsTool(BaseTool):
        name: str = "get_contract_details"
        description: str = "Get detailed information about a specific contract."
        
        def _run(self, contract_id: str) -> str:
            contracts = market_simulator.get_contracts()
            contract = next((c for c in contracts if c['id'] == contract_id), None)
            if contract:
                return json.dumps(contract, indent=2)
            return json.dumps({"error": f"Contract with ID {contract_id} not found"})
    
    class ProposeContractTool(BaseTool):
        name: str = "propose_contract"
        description: str = "Propose a new contract to a supplier."
        
        def _run(self, supplier_id: str, volume: int, price_per_pound: float, duration_months: int) -> str:
            suppliers = market_simulator.get_suppliers()
            supplier = next((s for s in suppliers if s['id'] == supplier_id), None)
            
            if not supplier:
                return json.dumps({"error": f"Supplier with ID {supplier_id} not found"})
            
            # Generate a new contract ID
            contract_id = f"contract_{supplier_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Calculate start and end dates
            start_date = datetime.now()
            end_date = start_date + timedelta(days=30 * int(duration_months))
            
            # Create the contract
            contract = {
                "id": contract_id,
                "supplier_id": supplier_id,
                "supplier_name": supplier.get('name', 'Unknown'),
                "status": "proposed",
                "volume_lbs": int(volume),
                "price_per_pound": float(price_per_pound),
                "total_value": round(int(volume) * float(price_per_pound), 2),
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "duration_months": int(duration_months),
                "terms": {
                    "payment_terms": "Net 30",
                    "quality_requirements": "Minimum 80/100 quality score",
                    "delivery_schedule": "Monthly",
                    "sustainability_requirements": "Rainforest Alliance Certified"
                },
                "proposed_date": datetime.now().strftime("%Y-%m-%d")
            }
            
            # Add the contract to the simulator
            market_simulator.add_contract(contract)
            
            return json.dumps(contract, indent=2)
    
    class NegotiateContractTool(BaseTool):
        name: str = "negotiate_contract"
        description: str = "Negotiate terms of a proposed contract."
        
        def _run(self, contract_id: str, counter_offer: Dict[str, Any]) -> str:
            contracts = market_simulator.get_contracts()
            contract = next((c for c in contracts if c['id'] == contract_id), None)
            
            if not contract:
                return json.dumps({"error": f"Contract with ID {contract_id} not found"})
            
            if contract['status'] != 'proposed':
                return json.dumps({"error": f"Contract with ID {contract_id} is not in 'proposed' status and cannot be negotiated"})
            
            # Update contract with counter offer
            for key, value in counter_offer.items():
                if key in contract and key not in ['id', 'supplier_id', 'supplier_name', 'status', 'proposed_date']:
                    contract[key] = value
            
            # Update total value if price or volume changed
            if 'price_per_pound' in counter_offer or 'volume_lbs' in counter_offer:
                contract['total_value'] = round(contract['volume_lbs'] * contract['price_per_pound'], 2)
            
            # Update the contract in the simulator
            market_simulator.update_contract(contract)
            
            return json.dumps(contract, indent=2)
    
    class FinalizeContractTool(BaseTool):
        name: str = "finalize_contract"
        description: str = "Finalize a proposed contract, changing its status to active."
        
        def _run(self, contract_id: str) -> str:
            contracts = market_simulator.get_contracts()
            contract = next((c for c in contracts if c['id'] == contract_id), None)
            
            if not contract:
                return json.dumps({"error": f"Contract with ID {contract_id} not found"})
            
            if contract['status'] != 'proposed':
                return json.dumps({"error": f"Contract with ID {contract_id} is not in 'proposed' status and cannot be finalized"})
            
            # Update contract status
            contract['status'] = 'active'
            contract['finalized_date'] = datetime.now().strftime("%Y-%m-%d")
            
            # Update the contract in the simulator
            market_simulator.update_contract(contract)
            
            return json.dumps(contract, indent=2)
    
    return [
        GetActiveContractsTool(),
        GetContractDetailsTool(),
        ProposeContractTool(),
        NegotiateContractTool(),
        FinalizeContractTool()
    ]

def create_order_tools(market_simulator) -> List[BaseTool]:
    """
    Create tools for the Order Management Agent.
    
    Args:
        market_simulator: The coffee market simulator instance
        
    Returns:
        List of tools for the order management agent
    """
    
    class GetActiveOrdersTool(BaseTool):
        name: str = "get_active_orders"
        description: str = "Get all active purchase orders."
        
        def _run(self, args: Optional[Dict] = None) -> str:
            orders = market_simulator.get_orders()
            active_orders = [o for o in orders if o['status'] in ['placed', 'in_transit', 'partially_delivered']]
            return json.dumps(active_orders, indent=2)
    
    class GetOrderDetailsTool(BaseTool):
        name: str = "get_order_details"
        description: str = "Get detailed information about a specific order."
        
        def _run(self, order_id: str) -> str:
            orders = market_simulator.get_orders()
            order = next((o for o in orders if o['id'] == order_id), None)
            if order:
                return json.dumps(order, indent=2)
            return json.dumps({"error": f"Order with ID {order_id} not found"})
    
    class CreateOrderTool(BaseTool):
        name: str = "create_order"
        description: str = "Create a new purchase order based on a contract."
        
        def _run(self, contract_id: str, volume: int) -> str:
            contracts = market_simulator.get_contracts()
            contract = next((c for c in contracts if c['id'] == contract_id), None)
            
            if not contract:
                return json.dumps({"error": f"Contract with ID {contract_id} not found"})
            
            if contract['status'] != 'active':
                return json.dumps({"error": f"Contract with ID {contract_id} is not active"})
            
            # Generate a new order ID
            order_id = f"order_{contract_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Calculate expected delivery date (30-60 days from now)
            order_date = datetime.now()
            expected_delivery = order_date + timedelta(days=random.randint(30, 60))
            
            # Create the order
            order = {
                "id": order_id,
                "contract_id": contract_id,
                "supplier_id": contract['supplier_id'],
                "supplier_name": contract['supplier_name'],
                "status": "placed",
                "volume_lbs": int(volume),
                "price_per_pound": contract['price_per_pound'],
                "total_value": round(int(volume) * contract['price_per_pound'], 2),
                "order_date": order_date.strftime("%Y-%m-%d"),
                "expected_delivery_date": expected_delivery.strftime("%Y-%m-%d"),
                "actual_delivery_date": None,
                "shipping_details": {
                    "carrier": random.choice(["OceanFreight", "AirCargo", "LandTransport"]),
                    "tracking_number": f"TRK{random.randint(100000, 999999)}",
                    "origin_port": f"Port of {market_simulator.get_country_for_supplier(contract['supplier_id'])}",
                    "destination_port": "Seattle, USA"
                }
            }
            
            # Add the order to the simulator
            market_simulator.add_order(order)
            
            return json.dumps(order, indent=2)
    
    class TrackOrderTool(BaseTool):
        name: str = "track_order"
        description: str = "Get the current status and tracking information for an order."
        
        def _run(self, order_id: str) -> str:
            orders = market_simulator.get_orders()
            order = next((o for o in orders if o['id'] == order_id), None)
            
            if not order:
                return json.dumps({"error": f"Order with ID {order_id} not found"})
            
            # Get updated tracking information
            tracking_info = market_simulator.get_order_tracking(order_id)
            
            return json.dumps(tracking_info, indent=2)
    
    class UpdateOrderStatusTool(BaseTool):
        name: str = "update_order_status"
        description: str = "Update the status of an existing order."
        
        def _run(self, order_id: str, new_status: str) -> str:
            valid_statuses = ['placed', 'in_transit', 'partially_delivered', 'delivered', 'cancelled', 'delayed']
            
            if new_status not in valid_statuses:
                return json.dumps({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"})
            
            orders = market_simulator.get_orders()
            order = next((o for o in orders if o['id'] == order_id), None)
            
            if not order:
                return json.dumps({"error": f"Order with ID {order_id} not found"})
            
            # Update order status
            order['status'] = new_status
            
            # If delivered, set actual delivery date
            if new_status == 'delivered':
                order['actual_delivery_date'] = datetime.now().strftime("%Y-%m-%d")
            
            # Update the order in the simulator
            market_simulator.update_order(order)
            
            return json.dumps(order, indent=2)
    
    return [
        GetActiveOrdersTool(),
        GetOrderDetailsTool(),
        CreateOrderTool(),
        TrackOrderTool(),
        UpdateOrderStatusTool()
    ]
