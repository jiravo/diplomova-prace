import pandas as pd
from config import *


def generate_machines():

    machines = []

    machine_id = 1

    for line in range(1, NUM_LINES + 1):
        for m in range(MACHINES_PER_LINE):

            machines.append(
                {
                    "machine_id": f"M{machine_id}",
                    "line_id": f"L{line}",
                    "machine_name": f"Machine_{machine_id}",
                    "machine_type": "CNC",
                    "manufacturer": "Siemens",
                    "installation_date": "2020-01-01",
                    "acquisition_cost": 250000,
                    "depreciation_rate": 0.1,
                    "max_units_per_hour": 120,
                    "planned_hours_per_day": 24,
                    "hourly_production_loss": 500,
                    "expected_lifetime_hours": 40000,
                }
            )

            machine_id += 1

    machines = pd.DataFrame(machines)
    machines.to_csv("data/Source/machines.csv", index=False)

    return machines
