import pandas as pd


def generate_fact_tables():

    # LOAD SOURCE
    sensor = pd.read_csv("data/Source/sensor_data.csv", parse_dates=["timestamp"])
    failures = pd.read_csv(
        "data/Source/failures.csv",
        parse_dates=["failure_time", "repair_start_time", "repair_end_time"],
    )
    maintenance = pd.read_csv(
        "data/Source/maintenance.csv", parse_dates=["start_time", "end_time"]
    )

    # LOAD DIMENSIONS
    time_dim = pd.read_csv("data/BI/D_Time.csv", parse_dates=["timestamp"])
    assetage_dim = pd.read_csv("data/BI/D_AssetAge.csv")
    failuretype_dim = pd.read_csv("data/BI/D_FailureType.csv")
    line_dim = pd.read_csv("data/BI/D_Line.csv")
    machine_dim = pd.read_csv("data/BI/D_Machine.csv")
    machinetype_dim = pd.read_csv("data/BI/D_MachineType.csv")
    maintenancetype_dim = pd.read_csv("data/BI/D_MaintenanceType.csv")
    severity_dim = pd.read_csv("data/BI/D_Severity.csv")
    spareparts_dim = pd.read_csv("data/BI/D_SparePart.csv")
    technician_dim = pd.read_csv("data/BI/D_Technician.csv")

    ###### F_EquipmentOperation

    F_EquipmentOperation = sensor[
        [
            "timestamp",
            "machine_id",
            "line_id",
            "is_running",
            "temperature",
            "vibration",
            "pressure",
            "load",
            "ambient_temperature",
            "produced_units",
            "defective_units",
            "planned_production",
            "operating_hours_since_maintenance",
            "machine_age_hours",
            "health_index",
        ]
    ]

    F_EquipmentOperation.to_csv("data/BI/F_EquipmentOperation.csv", index=False)

    ######## F_Failure

    failure_map = {
        "mechanical": "Mechanická",
        "overheating": "Přehřátí",
        "pressure": "Tlaková",
        "electrical": "Elektrická",
    }

    failures["failure_type"] = failures["failure_type"].map(failure_map)

    failures = failures.merge(
        failuretype_dim[["failure_type_id", "failure_type"]],
        on="failure_type",
        how="left",
    )

    failures = failures.drop(columns=["failure_type"])

    F_Failure = failures[
        [
            "failure_id",
            "machine_id",
            "line_id",
            "technician_id",
            "failure_type_id",
            "severity_id",
            "failure_time",
            "repair_start_time",
            "repair_end_time",
            "repair_time_minutes",
            "response_time_minutes",
            "downtime_minutes",
        ]
    ]

    F_Failure["downtime_hours"] = F_Failure["downtime_minutes"] / 60

    F_Failure.to_csv("data/BI/F_Failure.csv", index=False)

    ###### F_Maintenance

    F_Maintenance = maintenance[
        [
            "maintenance_id",
            "start_time",
            "end_time",
            "machine_id",
            "line_id",
            "technician_id",
            "maintenance_type_id",
            "related_failure_id",
            "duration_minutes",
            "labor_cost",
            "parts_cost",
            "part_id",
            "part_quantity",
        ]
    ]

    F_Maintenance["related_failure_id"] = F_Maintenance["related_failure_id"].astype(
        "Int64"
    )

    F_Maintenance["part_id"] = F_Maintenance["part_id"].astype("Int64")

    F_Maintenance["total_cost"] = (
        F_Maintenance["labor_cost"] + F_Maintenance["parts_cost"]
    )

    F_Maintenance["total_cost"] = F_Maintenance["total_cost"].astype(int)

    F_Maintenance.to_csv("data/BI/F_Maintenance.csv", index=False, sep=",", decimal=".")

    print("=== FK CHECK ===")

    check_fk(F_EquipmentOperation, machine_dim, "machine_id")
    check_fk(F_EquipmentOperation, line_dim, "line_id")

    check_fk(F_Failure, machine_dim, "machine_id")
    check_fk(F_Failure, line_dim, "line_id")
    check_fk(F_Failure, technician_dim, "technician_id")
    check_fk(F_Failure, failuretype_dim, "failure_type_id")
    check_fk(F_Failure, severity_dim, "severity_id")

    check_fk(F_Maintenance, machine_dim, "machine_id")
    check_fk(F_Maintenance, line_dim, "line_id")
    check_fk(F_Maintenance, technician_dim, "technician_id")
    check_fk(F_Maintenance, maintenancetype_dim, "maintenance_type_id")
    check_fk(F_Maintenance, spareparts_dim, "part_id")


def check_fk(fact, dim, key):

    missing = fact.loc[~fact[key].isin(dim[key])]

    if len(missing) > 0:
        print(f"FK ERROR: {key}")
        print(missing.head())
    else:
        print(f"{key} OK")
