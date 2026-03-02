# main.py
import pandas as pd
import numpy as np


from generators.generate_machines import generate_machines
from generators.generate_time import generate_time
from generators.factory_simulation import run_factory_simulation

np.random.seed(42)


def main():

    print("===================================")
    print("Factory Data Generation Started")
    print("===================================")

    print("Generating machines...")
    machines = generate_machines()

    print("Generating time...")
    time_df = generate_time()

    print("Running factory simulation...")
    sensor_data, failures = run_factory_simulation(machines, time_df)

    print("Saving data...")

    sensor_data.to_csv("data/Source/sensor_data.csv", index=False)

    failures.to_csv("data/Source/failures.csv", index=False)

    print("✅ Simulation finished!")

    print("===================================")
    print("Generation finished successfully")
    print("===================================")


if __name__ == "__main__":
    main()
