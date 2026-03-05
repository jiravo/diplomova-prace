import numpy as np
import pandas as pd

from generators.generate_D_Machine import generate_D_Machine
from generators.generate_time import generate_time
from generators.factory_simulation import run_factory_simulation
from generators.generate_D_MachineType import generate_machine_types
from generators.generate_D_AssetAge import generate_asset_age
from generators.generate_D_Line import generate_lines
from generators.generate_D_MaintenanceType import generate_D_MaintenanceType
from generators.generate_D_Severity import generate_D_Severity
from generators.generate_D_FailureType import generate_D_FailureType
from generators.generate_D_SpareParts import generate_D_SparePart
from generators.generate_D_Technician import generate_D_Technician
from generators.generate_maintenance import generate_maintenance
from generators.generate_maintenance import add_labor_and_parts


np.random.seed(42)


def main():

    print("===================================")
    print("Factory Data Generation Started")
    print("===================================")

    # TYPY STROJŮ
    print("Generating machine types...")
    generate_machine_types()

    # KATEGORIE STÁŘÍ STROJE
    print("Generating asset age dimension...")
    generate_asset_age()

    # LINKY
    print("Generating lines...")
    generate_lines()

    # TYP ÚDRŽBY
    print("Generating maintenance type...")
    generate_D_MaintenanceType()

    # KRITIČNOST
    print("Generating severity...")
    generate_D_Severity()

    # TYP PORUCHY
    print("Generating failure type...")
    generate_D_FailureType()

    # DÍLY
    print("Generating spare parts...")
    spare_parts_df = generate_D_SparePart()

    # ZAMĚSTNANCI
    print("Generating technicians...")
    technician_df = generate_D_Technician()

    # STROJE
    print("Generating D_Machine...")
    generate_D_Machine()

    machines = pd.read_csv("data/BI/D_Machine.csv")

    # LINKY
    print("Generating lines...")
    generate_lines()

    # ČAS
    print("Generating time...")
    time_df = generate_time()

    # SIMULACE TOVÁRNY !!!!!!!!!!!!!!!!!!!
    print("Running factory simulation...")
    sensor_data, failures = run_factory_simulation(machines, time_df)

    maintenance = generate_maintenance(failures, machines, time_df)

    maintenance = add_labor_and_parts(maintenance, technician_df, spare_parts_df)

    print("Saving data...")

    sensor_data.to_csv("data/Source/sensor_data.csv", index=False)

    failures.to_csv("data/Source/failures.csv", index=False)

    maintenance.to_csv("data/Source/maintenance.csv", index=False)

    print("✅ Simulation finished!")

    print("===================================")
    print("Generation finished successfully")
    print("===================================")


if __name__ == "__main__":
    main()
