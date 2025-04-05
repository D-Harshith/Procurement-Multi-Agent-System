import random
from datetime import datetime, timedelta
import json
import copy
from typing import List, Dict, Any

class CoffeeMarketSimulator:
    """
    Simulates the coffee market environment for the Starbucks Procurement Multi-Agent System.
    """
    
    def __init__(self, initial_data):
        """
        Initialize the coffee market simulator with initial data.
        
        Args:
            initial_data: Dict containing suppliers, contracts, orders, and market conditions
        """
        self.suppliers = initial_data["suppliers"]
        self.contracts = initial_data["contracts"]
        self.orders = initial_data["orders"]
        self.market_conditions = initial_data["market_conditions"]
        
        self.simulation_date = datetime.now()
        self.simulation_step = 0
        
        # Track changes since last step
        self.changes = {
            "suppliers": [],
            "contracts": [],
            "orders": [],
            "market_conditions": {}
        }
        
        # Map of regions to countries for supplier location data
        self.region_to_country = {
            "Central America": ["Guatemala", "Costa Rica", "Honduras", "Nicaragua", "El Salvador", "Panama"],
            "South America": ["Brazil", "Colombia", "Peru", "Ecuador", "Bolivia"],
            "Africa": ["Ethiopia", "Kenya", "Rwanda", "Tanzania", "Uganda", "Burundi"],
            "Asia": ["Vietnam", "Indonesia", "India", "Papua New Guinea", "Thailand", "Laos"]
        }
    
    def simulate_step(self):
        """
        Simulate one step in the coffee market environment.
        """
        # Increment simulation step
        self.simulation_step += 1
        
        # Advance simulation date (each step is 1 day)
        self.simulation_date += timedelta(days=1)
        
        # Reset changes
        self.changes = {
            "suppliers": [],
            "contracts": [],
            "orders": [],
            "market_conditions": {}
        }
        
        # Update market conditions
        self._update_market_conditions()
        
        # Update orders (progress delivery, etc.)
        self._update_orders()
        
        # Update suppliers (occasionally)
        if random.random() < 0.2:  # 20% chance each step
            self._update_suppliers()
            
        # Ensure we have at least one active contract for the Order Agent to use
        if len([c for c in self.contracts if c['status'] == 'active']) == 0:
            if random.random() < 0.5:  # 50% chance to create a contract if none exist
                self._create_sample_contract()
    
    def _update_market_conditions(self):
        """
        Update coffee market conditions.
        """
        # Update date
        self.market_conditions["date"] = self.simulation_date.isoformat()
        
        # Update average price with some volatility
        current_price = self.market_conditions["average_price"]
        
        # Determine price change direction and magnitude
        # More likely to follow the current trend, but with some randomness
        if self.market_conditions["price_trend"] == "Rising":
            change_pct = random.uniform(-0.01, 0.03)  # -1% to +3%
        elif self.market_conditions["price_trend"] == "Falling":
            change_pct = random.uniform(-0.03, 0.01)  # -3% to +1%
        else:  # Stable
            change_pct = random.uniform(-0.015, 0.015)  # -1.5% to +1.5%
        
        # Apply the price change
        new_price = round(current_price * (1 + change_pct), 2)
        
        # Ensure price stays within reasonable bounds
        new_price = max(3.0, min(10.0, new_price))
        
        # Update the price
        self.market_conditions["average_price"] = new_price
        
        # Update price history
        self.market_conditions["price_history"].append({
            "date": self.simulation_date.isoformat(),
            "price": new_price
        })
        
        # Keep only the last 30 days of history
        if len(self.market_conditions["price_history"]) > 30:
            self.market_conditions["price_history"] = self.market_conditions["price_history"][-30:]
        
        # Update price trend based on recent history
        history = self.market_conditions["price_history"]
        if len(history) >= 5:
            recent_prices = [entry["price"] for entry in history[-5:]]
            if recent_prices[-1] > recent_prices[0] * 1.02:
                self.market_conditions["price_trend"] = "Rising"
            elif recent_prices[-1] < recent_prices[0] * 0.98:
                self.market_conditions["price_trend"] = "Falling"
            else:
                self.market_conditions["price_trend"] = "Stable"
        
        # Update regional prices based on the average price change
        for region in self.market_conditions["regional_prices"]:
            regional_price = self.market_conditions["regional_prices"][region]
            # Apply similar change with some variation
            regional_change = change_pct + random.uniform(-0.01, 0.01)
            new_regional_price = round(regional_price * (1 + regional_change), 2)
            self.market_conditions["regional_prices"][region] = new_regional_price
        
        # Update bean prices similarly
        for bean in self.market_conditions["bean_prices"]:
            bean_price = self.market_conditions["bean_prices"][bean]
            # Apply similar change with some variation
            bean_change = change_pct + random.uniform(-0.01, 0.01)
            new_bean_price = round(bean_price * (1 + bean_change), 2)
            self.market_conditions["bean_prices"][bean] = new_bean_price
        
        # Occasionally update market factors (10% chance each step)
        if random.random() < 0.1:
            factor_index = random.randint(0, len(self.market_conditions["market_factors"]) - 1)
            factor = self.market_conditions["market_factors"][factor_index]
            
            # Update status
            factor["status"] = random.choice(["Favorable", "Mixed", "Concerning"])
            factor["impact"] = random.choice(["Minimal", "Moderate", "Significant"])
            
            # Update details based on factor name
            if factor["name"] == "Weather Conditions":
                factor["details"] = random.choice([
                    "Ideal rainfall in major growing regions",
                    "Drought conditions in parts of Brazil",
                    "Excessive rainfall in Colombia affecting harvest",
                    "Normal seasonal patterns across most regions",
                    "Frost concerns in Brazil",
                    "Hurricane damage in Central America"
                ])
            elif factor["name"] == "Political Stability":
                factor["details"] = random.choice([
                    "No major political disruptions in key regions",
                    "Political tensions in Ethiopia affecting exports",
                    "Trade policy changes impacting shipping costs",
                    "Labor disputes in Colombia affecting production",
                    "New export regulations in Vietnam",
                    "Currency devaluation in Brazil affecting prices"
                ])
            elif factor["name"] == "Global Demand":
                factor["details"] = random.choice([
                    "Steady increase in global coffee consumption",
                    "Shifting consumer preferences toward specialty coffee",
                    "Economic slowdown affecting cafe sales",
                    "New markets emerging in Asia",
                    "Increased home consumption trends",
                    "Seasonal demand fluctuations"
                ])
            
            # Update the factor in the market conditions
            self.market_conditions["market_factors"][factor_index] = factor
        
        # Occasionally update forecast (5% chance each step)
        if random.random() < 0.05:
            self.market_conditions["forecast"] = {
                "short_term": random.choice(["Price increase expected", "Stable prices likely", "Price decrease expected"]),
                "long_term": random.choice(["Upward trend", "Stable market", "Downward pressure", "Increased volatility"])
            }
        
        # Record changes
        self.changes["market_conditions"] = {
            "new_price": new_price,
            "old_price": current_price,
            "change_pct": change_pct
        }
    
    def _update_orders(self):
        """
        Update order status based on delivery timelines.
        """
        for i, order in enumerate(self.orders):
            # Skip orders that are already delivered or cancelled
            if order["status"] in ["delivered", "cancelled"]:
                continue
            
            # Calculate days until expected delivery
            # Handle both expected_delivery and expected_delivery_date fields for compatibility
            if "expected_delivery" in order:
                expected_delivery_str = order["expected_delivery"]
            elif "expected_delivery_date" in order:
                expected_delivery_str = order["expected_delivery_date"]
            else:
                continue  # Skip orders without delivery date
                
            # Convert string date to datetime object
            try:
                # Handle ISO format with or without Z
                if 'Z' in expected_delivery_str:
                    expected_delivery = datetime.fromisoformat(expected_delivery_str.replace('Z', ''))
                else:
                    expected_delivery = datetime.fromisoformat(expected_delivery_str)
            except ValueError:
                # Handle simple date format (YYYY-MM-DD)
                expected_delivery = datetime.strptime(expected_delivery_str, "%Y-%m-%d")
                
            days_until_delivery = (expected_delivery - self.simulation_date).days
            
            # Update order status based on timeline
            if order["status"] == "pending" and days_until_delivery <= 30:
                # Order has been processed and is now in transit
                if random.random() < 0.8:  # 80% chance of normal progression
                    self.orders[i]["status"] = "in_transit"
                    self.changes["orders"].append({
                        "id": order["id"],
                        "old_status": "pending",
                        "new_status": "in_transit"
                    })
                elif random.random() < 0.5:  # 10% chance of delay (0.5 * 0.2)
                    self.orders[i]["status"] = "delayed"
                    # Add random delay
                    delay_days = random.randint(5, 15)
                    new_delivery = expected_delivery + timedelta(days=delay_days)
                    
                    # Update the delivery date field that exists in the order
                    if "expected_delivery" in order:
                        self.orders[i]["expected_delivery"] = new_delivery.isoformat()
                    elif "expected_delivery_date" in order:
                        self.orders[i]["expected_delivery_date"] = new_delivery.strftime("%Y-%m-%d")
                    
                    self.changes["orders"].append({
                        "id": order["id"],
                        "old_status": "pending",
                        "new_status": "delayed",
                        "delay_days": delay_days
                    })
            
            elif order["status"] == "in_transit" and days_until_delivery <= 0:
                # Order has arrived
                self.orders[i]["status"] = "delivered"
                self.changes["orders"].append({
                    "id": order["id"],
                    "old_status": "in_transit",
                    "new_status": "delivered"
                })
            
            elif order["status"] == "delayed":
                # Delayed orders have a chance to resume transit
                if random.random() < 0.3:  # 30% chance each step
                    self.orders[i]["status"] = "in_transit"
                    self.changes["orders"].append({
                        "id": order["id"],
                        "old_status": "delayed",
                        "new_status": "in_transit"
                    })
    
    def _update_suppliers(self):
        """
        Update supplier information occasionally.
        """
        # Select a random supplier to update
        if len(self.suppliers) > 0:
            supplier_index = random.randint(0, len(self.suppliers) - 1)
            supplier = self.suppliers[supplier_index]
            
            # Determine what to update
            update_type = random.choice(["quality", "reliability", "sustainability", "capacity"])
            
            old_value = None
            new_value = None
            
            if update_type == "quality":
                old_value = supplier["quality_score"]
                # Small random change to quality score
                change = random.uniform(-0.5, 0.5)
                new_value = round(max(5.0, min(10.0, old_value + change)), 1)
                self.suppliers[supplier_index]["quality_score"] = new_value
            
            elif update_type == "reliability":
                old_value = supplier["reliability_score"]
                # Small random change to reliability score
                change = random.uniform(-0.5, 0.5)
                new_value = round(max(5.0, min(10.0, old_value + change)), 1)
                self.suppliers[supplier_index]["reliability_score"] = new_value
            
            elif update_type == "sustainability":
                old_value = supplier["sustainability_score"]
                # Small random change to sustainability score
                change = random.uniform(-0.5, 0.5)
                new_value = round(max(5.0, min(10.0, old_value + change)), 1)
                self.suppliers[supplier_index]["sustainability_score"] = new_value
            
            elif update_type == "capacity":
                old_value = supplier["capacity_kg_per_year"]
                # Change capacity by -10% to +10%
                change_pct = random.uniform(-0.1, 0.1)
                new_value = int(old_value * (1 + change_pct))
                self.suppliers[supplier_index]["capacity_kg_per_year"] = new_value
            
            # Record the change
            self.changes["suppliers"].append({
                "id": supplier["id"],
                "name": supplier["name"],
                "update_type": update_type,
                "old_value": old_value,
                "new_value": new_value
            })
    
    def get_suppliers(self) -> List[Dict[str, Any]]:
        """
        Get the current list of suppliers.
        
        Returns:
            List of supplier data
        """
        return copy.deepcopy(self.suppliers)
    
    def get_contracts(self) -> List[Dict[str, Any]]:
        """
        Get the current list of contracts.
        
        Returns:
            List of contract data
        """
        return copy.deepcopy(self.contracts)
    
    def get_orders(self) -> List[Dict[str, Any]]:
        """
        Get the current list of orders.
        
        Returns:
            List of order data
        """
        return copy.deepcopy(self.orders)
    
    def get_market_conditions(self) -> Dict[str, Any]:
        """
        Get the current market conditions.
        
        Returns:
            Dict containing market condition data
        """
        return copy.deepcopy(self.market_conditions)
    
    def add_contract(self, contract: Dict[str, Any]):
        """
        Add a new contract.
        
        Args:
            contract: Contract data to add
        """
        self.contracts.append(contract)
        self.changes["contracts"].append({
            "action": "add",
            "contract_id": contract["id"]
        })
    
    def update_contract_status(self, contract_id: str, status: str):
        """
        Update the status of a contract.
        
        Args:
            contract_id: ID of the contract to update
            status: New status value
        """
        for i, contract in enumerate(self.contracts):
            if contract["id"] == contract_id:
                old_status = contract["status"]
                self.contracts[i]["status"] = status
                self.changes["contracts"].append({
                    "action": "update_status",
                    "contract_id": contract_id,
                    "old_status": old_status,
                    "new_status": status
                })
                break
    
    def add_order(self, order: Dict[str, Any]):
        """
        Add a new order to the system.
        
        Args:
            order: The order data to add
        """
        # Add the order to our list
        self.orders.append(order)
        
        # Record the change
        self.changes["orders"].append({
            "id": order["id"],
            "action": "created",
            "supplier": order.get("supplier_name", "Unknown"),
            "volume": order.get("volume_lbs", 0)
        })
    
    def update_order_status(self, order_id: str, status: str):
        """
        Update the status of an order.
        
        Args:
            order_id: ID of the order to update
            status: New status value
        """
        for i, order in enumerate(self.orders):
            if order["id"] == order_id:
                old_status = order["status"]
                self.orders[i]["status"] = status
                self.changes["orders"].append({
                    "action": "update_status",
                    "order_id": order_id,
                    "old_status": old_status,
                    "new_status": status
                })
                break
    
    def update_order_expected_delivery(self, order_id: str, expected_delivery: str):
        """
        Update the expected delivery date of an order.
        
        Args:
            order_id: ID of the order to update
            expected_delivery: New expected delivery date
        """
        for i, order in enumerate(self.orders):
            if order["id"] == order_id:
                old_delivery = order["expected_delivery"]
                # Update the delivery date field that exists in the order
                if "expected_delivery" in order:
                    self.orders[i]["expected_delivery"] = expected_delivery
                elif "expected_delivery_date" in order:
                    self.orders[i]["expected_delivery_date"] = expected_delivery
                
                self.changes["orders"].append({
                    "action": "update_delivery",
                    "order_id": order_id,
                    "old_delivery": old_delivery,
                    "new_delivery": expected_delivery
                })
                break
    
    def get_changes(self) -> Dict[str, Any]:
        """
        Get changes since the last simulation step.
        
        Returns:
            Dict containing changes to suppliers, contracts, orders, and market conditions
        """
        return copy.deepcopy(self.changes)
    
    def get_country_for_region(self, region: str) -> str:
        """
        Get a random country for a given coffee-growing region.
        
        Args:
            region: The coffee-growing region
            
        Returns:
            A country name from that region
        """
        if region in self.region_to_country:
            return random.choice(self.region_to_country[region])
        return "Unknown"
    
    def get_country_for_supplier(self, supplier_id: str) -> str:
        """
        Get the country where a supplier is located.
        
        Args:
            supplier_id: ID of the supplier
            
        Returns:
            The country where the supplier is located
        """
        supplier = next((s for s in self.suppliers if s['id'] == supplier_id), None)
        if supplier and 'country' in supplier:
            return supplier['country']
        elif supplier and 'region' in supplier:
            return self.get_country_for_region(supplier['region'])
        return "Unknown"
    
    def get_order_tracking(self, order_id: str) -> Dict[str, Any]:
        """
        Get tracking information for a specific order.
        
        Args:
            order_id: ID of the order to track
            
        Returns:
            Order tracking information
        """
        order = next((o for o in self.orders if o['id'] == order_id), None)
        
        if not order:
            return {"error": f"Order with ID {order_id} not found"}
        
        # Generate tracking information based on order status
        status = order['status']
        tracking_info = {
            "order_id": order_id,
            "supplier_name": order.get('supplier_name', 'Unknown Supplier'),
            "current_status": status,
            "status_updated": datetime.now().strftime("%Y-%m-%d"),
            "shipping_details": order.get('shipping_details', {})
        }
        
        if status == 'placed':
            tracking_info["location"] = "Supplier facility"
            tracking_info["status_details"] = "Order is being processed by the supplier"
            tracking_info["next_update_expected"] = (datetime.now() + timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d")
        
        elif status == 'in_transit':
            locations = ["Origin port", "Atlantic Ocean", "Pacific Ocean", "Destination port", "Customs clearance", "Local distribution center"]
            tracking_info["location"] = random.choice(locations)
            tracking_info["status_details"] = "Order is in transit to destination"
            tracking_info["estimated_arrival"] = order.get('expected_delivery_date', 'Unknown')
            tracking_info["transportation_method"] = order.get('shipping_details', {}).get('carrier', 'Unknown')
        
        elif status == 'delayed':
            tracking_info["location"] = random.choice(["Origin port", "Customs clearance", "International waters", "Transshipment port"])
            tracking_info["status_details"] = random.choice([
                "Weather-related shipping delay",
                "Customs processing delay",
                "Logistics coordination issue",
                "Documentation discrepancy"
            ])
            tracking_info["delay_duration"] = f"{random.randint(3, 15)} days"
            original_date = datetime.strptime(order.get('expected_delivery_date', datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
            tracking_info["revised_delivery"] = (original_date + timedelta(days=random.randint(3, 15))).strftime("%Y-%m-%d")
        
        elif status == 'delivered' or status == 'partially_delivered':
            tracking_info["location"] = "Starbucks warehouse"
            tracking_info["delivery_date"] = order.get('actual_delivery_date', datetime.now().strftime("%Y-%m-%d"))
            tracking_info["received_by"] = "Warehouse Manager"
            tracking_info["quality_check_status"] = random.choice(["Pending", "In progress", "Completed - Passed", "Completed - Minor issues"])
            
            if status == 'partially_delivered':
                tracking_info["delivery_percentage"] = f"{random.randint(50, 95)}%"
                tracking_info["remaining_delivery_expected"] = (datetime.now() + timedelta(days=random.randint(7, 21))).strftime("%Y-%m-%d")
        
        return tracking_info

    def _create_sample_contract(self):
        """
        Create a sample contract to ensure the Order Agent has something to work with.
        """
        # Select a random supplier
        if not self.suppliers:
            return
            
        supplier = random.choice(self.suppliers)
        
        # Generate a new contract ID
        contract_id = f"contract_{supplier['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Calculate contract duration (3-12 months)
        start_date = self.simulation_date
        end_date = start_date + timedelta(days=random.randint(90, 365))
        
        # Calculate price based on market conditions and supplier quality
        base_price = self.market_conditions["average_price"]
        quality_factor = supplier.get('quality_score', 7.0) / 10.0  # Higher quality = higher price
        contract_price = round(base_price * (0.9 + quality_factor * 0.3), 2)  # Price adjustment based on quality
        
        # Create the contract
        contract = {
            "id": contract_id,
            "supplier_id": supplier['id'],
            "supplier_name": supplier['name'],
            "status": "active",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "price_per_pound": contract_price,
            "volume_range": {
                "min_lbs": random.randint(5000, 10000),
                "max_lbs": random.randint(15000, 30000)
            },
            "bean_types": supplier.get('bean_types', ['Arabica']),
            "terms": {
                "payment_terms": random.choice(["Net 30", "Net 45", "Net 60"]),
                "delivery_terms": random.choice(["FOB", "CIF", "EXW"]),
                "quality_requirements": "SCA score 80+",
                "sustainability_requirements": random.choice([
                    "Rainforest Alliance Certified", 
                    "Organic Certified",
                    "Fair Trade Certified",
                    "Standard Practices"
                ])
            }
        }
        
        # Add the contract to the simulator
        self.contracts.append(contract)
        
        # Record the change
        self.changes["contracts"].append({
            "id": contract_id,
            "action": "created",
            "supplier": supplier['name']
        })
        
        print(f"Created sample contract with {supplier['name']} for {contract_price}/lb")
