import random
from datetime import datetime, timedelta
import json

def generate_initial_data():
    """
    Generate initial data for the Starbucks Procurement Multi-Agent System.
    
    Returns:
        Dict containing suppliers, contracts, orders, and market conditions
    """
    # Generate suppliers
    suppliers = generate_suppliers()
    
    # Generate contracts (initially empty)
    contracts = []
    
    # Generate orders (initially empty)
    orders = []
    
    # Generate market conditions
    market_conditions = generate_market_conditions()
    
    return {
        "suppliers": suppliers,
        "contracts": contracts,
        "orders": orders,
        "market_conditions": market_conditions
    }

def generate_suppliers(count=10):
    """
    Generate a list of coffee suppliers.
    
    Args:
        count: Number of suppliers to generate
        
    Returns:
        List of supplier data
    """
    regions = [
        {"name": "Ethiopia", "beans": ["Arabica", "Typica", "Bourbon"], "quality_range": (7.5, 9.5)},
        {"name": "Colombia", "beans": ["Arabica", "Bourbon", "Typica"], "quality_range": (7.0, 9.0)},
        {"name": "Brazil", "beans": ["Arabica", "Bourbon", "Robusta"], "quality_range": (6.5, 8.5)},
        {"name": "Vietnam", "beans": ["Robusta", "Arabica"], "quality_range": (6.0, 8.0)},
        {"name": "Guatemala", "beans": ["Arabica", "Bourbon", "Typica"], "quality_range": (7.0, 9.0)},
        {"name": "Costa Rica", "beans": ["Arabica", "Gesha", "Typica"], "quality_range": (7.5, 9.5)},
        {"name": "Kenya", "beans": ["Arabica", "SL28", "SL34"], "quality_range": (7.5, 9.5)},
        {"name": "Indonesia", "beans": ["Arabica", "Robusta", "Typica"], "quality_range": (6.5, 8.5)}
    ]
    
    certifications = ["Organic", "Fair Trade", "Rainforest Alliance", "UTZ", "Bird Friendly"]
    
    suppliers = []
    
    for i in range(1, count + 1):
        region = random.choice(regions)
        region_name = region["name"]
        
        # Select 1-2 bean types for this supplier
        bean_count = random.randint(1, 2)
        bean_types = random.sample(region["beans"], k=min(bean_count, len(region["beans"])))
        
        # Select 0-3 certifications
        cert_count = random.randint(0, 3)
        supplier_certifications = random.sample(certifications, k=min(cert_count, len(certifications)))
        
        # Generate quality score within the region's typical range
        quality_min, quality_max = region["quality_range"]
        quality_score = round(random.uniform(quality_min, quality_max), 1)
        
        # Generate capacity
        capacity = random.randint(10, 100) * 1000  # 10K-100K kg
        
        supplier = {
            "id": f"S{i}",
            "name": f"{region_name} Coffee Cooperative {i}",
            "region": region_name,
            "bean_types": bean_types,
            "certifications": supplier_certifications,
            "quality_score": quality_score,
            "capacity_kg_per_year": capacity,
            "reliability_score": round(random.uniform(6.0, 9.5), 1),
            "years_in_business": random.randint(3, 50),
            "sustainability_score": round(random.uniform(5.0, 10.0), 1)
        }
        
        suppliers.append(supplier)
    
    return suppliers

def generate_market_conditions():
    """
    Generate initial coffee market conditions.
    
    Returns:
        Dict containing market condition data
    """
    current_date = datetime.now()
    
    # Base price per kg for Arabica
    base_price = round(random.uniform(4.0, 6.0), 2)
    
    # Generate price history (last 30 days)
    price_history = []
    temp_price = base_price
    
    for i in range(30, 0, -1):
        date = current_date - timedelta(days=i)
        # Random daily fluctuation between -3% and +3%
        change_pct = random.uniform(-0.03, 0.03)
        temp_price = round(temp_price * (1 + change_pct), 2)
        
        price_history.append({
            "date": date.isoformat(),
            "price": temp_price
        })
    
    # Generate regional price variations
    regions = ["Ethiopia", "Colombia", "Brazil", "Vietnam", "Guatemala", "Costa Rica", "Kenya", "Indonesia"]
    regional_prices = {}
    
    for region in regions:
        # Random variation between -10% and +15% from base price
        variation = random.uniform(-0.10, 0.15)
        regional_prices[region] = round(base_price * (1 + variation), 2)
    
    # Generate bean type price variations
    bean_types = ["Arabica", "Robusta", "Bourbon", "Typica", "Gesha"]
    bean_prices = {}
    
    bean_prices["Arabica"] = base_price
    bean_prices["Robusta"] = round(base_price * random.uniform(0.7, 0.9), 2)
    bean_prices["Bourbon"] = round(base_price * random.uniform(1.05, 1.2), 2)
    bean_prices["Typica"] = round(base_price * random.uniform(1.0, 1.15), 2)
    bean_prices["Gesha"] = round(base_price * random.uniform(1.5, 2.5), 2)
    
    # Market condition factors
    factors = [
        {
            "name": "Weather Conditions",
            "status": random.choice(["Favorable", "Mixed", "Concerning"]),
            "impact": random.choice(["Minimal", "Moderate", "Significant"]),
            "details": random.choice([
                "Ideal rainfall in major growing regions",
                "Drought conditions in parts of Brazil",
                "Excessive rainfall in Colombia affecting harvest",
                "Normal seasonal patterns across most regions"
            ])
        },
        {
            "name": "Political Stability",
            "status": random.choice(["Stable", "Some Concerns", "Unstable"]),
            "impact": random.choice(["Minimal", "Moderate", "Significant"]),
            "details": random.choice([
                "No major political disruptions in key regions",
                "Political tensions in Ethiopia affecting exports",
                "Trade policy changes impacting shipping costs",
                "Labor disputes in Colombia affecting production"
            ])
        },
        {
            "name": "Global Demand",
            "status": random.choice(["Growing", "Stable", "Declining"]),
            "impact": random.choice(["Minimal", "Moderate", "Significant"]),
            "details": random.choice([
                "Steady increase in global coffee consumption",
                "Shifting consumer preferences toward specialty coffee",
                "Economic slowdown affecting cafe sales",
                "New markets emerging in Asia"
            ])
        }
    ]
    
    # Compile market conditions
    market_conditions = {
        "date": current_date.isoformat(),
        "average_price": base_price,
        "price_trend": random.choice(["Rising", "Stable", "Falling"]),
        "price_history": price_history,
        "regional_prices": regional_prices,
        "bean_prices": bean_prices,
        "market_factors": factors,
        "forecast": {
            "short_term": random.choice(["Price increase expected", "Stable prices likely", "Price decrease expected"]),
            "long_term": random.choice(["Upward trend", "Stable market", "Downward pressure", "Increased volatility"])
        }
    }
    
    return market_conditions
