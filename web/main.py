# web/main.py
import sys
import os
from datetime import datetime

print(f"[DEBUG] Starting main.py")
print(f"[DEBUG] Current working directory: {os.getcwd()}")
print(f"[DEBUG] sys.path: {sys.path}")

# Set the project root as the base directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
print(f"[DEBUG] Added project root to sys.path: {project_root}")

# Import your modules
try:
    from simulation.data_generator import generate_initial_data
    from simulation.market_simulator import CoffeeMarketSimulator
    from agents.crew_manager import StarbucksProcurementCrew
    print("[DEBUG] Successfully imported all modules")
except ImportError as e:
    print(f"[DEBUG] ImportError: {e}")
    sys.exit(1)

def run_crew():
    print("[DEBUG] Inside run_crew")
    initial_data = generate_initial_data()
    market_simulator = CoffeeMarketSimulator(initial_data)
    crew = StarbucksProcurementCrew(market_simulator)
    result = crew.run()
    print(f"[Final Outcome] {datetime.now().isoformat()} {result}")

if __name__ == "__main__":
    print("[DEBUG] Starting run_crew")
    run_crew()
    print("[DEBUG] Finished run_crew")
    sys.stdout.flush()