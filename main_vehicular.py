from edge_sim_py import *
import glob
import os
import argparse

from vehicular_runtime.scheduler_loop import DynamicSchedulerLoop
from config import *

# ----------------------------------------------------
# Load dataset (INFRASTRUCTURE ONLY)
# ----------------------------------------------------
def load_first_dataset():
    dataset_files = glob.glob("datasets/*.json")

    if not dataset_files:
        print("❌ No datasets found in /datasets folder.")
        print("Run generate_dynamic_scenario.py first.")
        exit()

    print(f"📂 Using dataset: {dataset_files[0]}")
    print("🧠 Dataset contains ONLY infrastructure.")
    print("🚗 Vehicles + Users will be created dynamically from SUMO.\n")

    return dataset_files[0]

# ----------------------------------------------------
# Build data dictionary used by scheduler
# ----------------------------------------------------
def build_data_dict():
    data = {
        'BaseStation': BaseStation,
        'EdgeServer': EdgeServer,
        'User': User,  # Will be overridden dynamically
        'NetworkSwitch': NetworkSwitch,
        'NetworkLink': NetworkLink
    }
    return data

# ----------------------------------------------------
# Prepare output folders
# ----------------------------------------------------
def prepare_output_dirs():
    os.makedirs("vehicular_outputs", exist_ok=True)
    os.makedirs("vehicular_outputs/logs", exist_ok=True)
    os.makedirs("vehicular_outputs/csv", exist_ok=True)

# ----------------------------------------------------
# MAIN ENTRY
# ----------------------------------------------------
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--gui", action="store_true", help="Run SUMO with GUI")
    args = parser.parse_args()

    print("\n==============================")
    print("🚗 VEHICULAR FOG ORCHESTRATION")
    print("==============================")

    prepare_output_dirs()

    # 1️⃣ Load infrastructure dataset
    dataset_path = load_first_dataset()

    # 2️⃣ Initialize EdgeSimPy simulator
    simulator = Simulator()
    simulator.initialize(input_file=dataset_path)

    # 3️⃣ Prepare data dictionary for algorithms
    data = build_data_dict()

    # 4️⃣ Start dynamic vehicular orchestration loop
    runtime = DynamicSchedulerLoop(simulator, data, use_gui=args.gui)
    runtime.run()
