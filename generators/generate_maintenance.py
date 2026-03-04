import pandas as pd
import numpy as np


def generate_maintenance(failures_df, machines_df, time_df):

    # =========================
    # CORRECTIVE MAINTENANCE
    # =========================
    reactive = failures_df.copy()

    reactive["maintenance_type_id"] = 1
    reactive["start_time"] = reactive["repair_start_time"]
    reactive["end_time"] = reactive["repair_end_time"]
    reactive["duration_minutes"] = reactive["repair_time_minutes"]
    reactive["related_failure_id"] = reactive["failure_id"]

    reactive = reactive[
        [
            "line_id",
            "machine_id",
            "maintenance_type_id",
            "related_failure_id",
            "start_time",
            "end_time",
            "duration_minutes",
            "technician_id",
        ]
    ]

    # =========================
    # SHORT PREVENTIVE (14 dní)
    # =========================
    preventive_short = []

    for _, machine in machines_df.iterrows():

        machine_id = machine["machine_id"]
        line_id = machine["line_id"]

        current_time = time_df["timestamp"].min()
        end_time_limit = time_df["timestamp"].max()

        while current_time < end_time_limit:

            current_time += pd.Timedelta(days=np.random.randint(10, 15))

            preventive_short.append(
                {
                    "line_id": line_id,
                    "machine_id": machine_id,
                    "maintenance_type_id": 1,
                    "related_failure_id": None,
                    "start_time": current_time,
                    "duration_minutes": np.random.randint(20, 60),
                    "technician_id": np.random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10]),
                }
            )

    preventive_short = pd.DataFrame(preventive_short)

    # =========================
    # LONG PREVENTIVE (3–6 měsíců)
    # =========================
    preventive_long = []

    for _, machine in machines_df.iterrows():

        machine_id = machine["machine_id"]
        line_id = machine["line_id"]

        current_time = time_df["timestamp"].min()
        end_time_limit = time_df["timestamp"].max()

        while current_time < end_time_limit:

            current_time += pd.Timedelta(days=np.random.randint(90, 180))

            preventive_long.append(
                {
                    "line_id": line_id,
                    "machine_id": machine_id,
                    "maintenance_type_id": 2,
                    "related_failure_id": None,
                    "start_time": current_time,
                    "duration_minutes": np.random.randint(120, 480),
                    "technician_id": np.random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10]),
                }
            )

    preventive_long = pd.DataFrame(preventive_long)

    # =========================
    # SPOJENÍ VŠECH MAINTENANCE
    # =========================
    maintenance = pd.concat(
        [reactive, preventive_short, preventive_long], ignore_index=True
    )

    # =========================
    # END TIME
    # =========================
    maintenance["end_time"] = maintenance["start_time"] + pd.to_timedelta(
        maintenance["duration_minutes"], unit="m"
    )

    # =========================
    # MAINTENANCE ID
    # =========================
    maintenance.insert(0, "maintenance_id", range(1, len(maintenance) + 1))

    return maintenance
