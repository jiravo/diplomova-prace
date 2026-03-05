"""import pandas as pd
import numpy as np


def generate_maintenance(failures_df, machines_df, time_df):

    # =========================
    # REACTIVE MAINTENANCE
    # =========================
    reactive = failures_df.copy()

    reactive["maintenance_type_id"] = 2
    reactive["start_time"] = reactive["repair_start_time"]
    reactive["end_time"] = reactive["repair_end_time"]
    reactive["duration_minutes"] = reactive["repair_time_minutes"]
    reactive["related_failure_id"] = reactive["failure_id"]

    reactive = reactive[
        [
            "machine_id",
            "line_id",
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

        machine_maintenance = []

        machine_failures = failures_df[failures_df["machine_id"] == machine_id]

        current_day = time_df["timestamp"].min().normalize()
        end_time_limit = time_df["timestamp"].max()

        attempts = 0

        while True:

            attempts += 1
            if attempts > 100:
                break

            current_day += pd.Timedelta(days=np.random.randint(10, 15))

            next_time = pd.Timestamp(
                year=current_day.year,
                month=current_day.month,
                day=current_day.day,
                hour=np.random.randint(6, 22),
                minute=np.random.randint(0, 60),
            )

            if next_time > end_time_limit:
                break

            duration = np.random.randint(20, 60)

            # ===== KOLIZE S PORUCHOU =====
            collision = machine_failures[
                (machine_failures["failure_time"] - pd.Timedelta(hours=6) <= next_time)
                & (
                    machine_failures["repair_end_time"] + pd.Timedelta(hours=6)
                    >= next_time
                )
            ]

            if not collision.empty:
                continue

            # ===== KOLIZE S EXISTUJÍCÍ MAINTENANCE =====
            overlap = False

            for m in machine_maintenance:

                m_start = m["start_time"]
                m_end = m_start + pd.Timedelta(minutes=m["duration_minutes"])

                new_end = next_time + pd.Timedelta(minutes=duration)

                if (next_time < m_end) and (new_end > m_start):
                    overlap = True
                    break

            if overlap:
                continue
            # ==========================================

            preventive_short.append(
                {
                    "line_id": line_id,
                    "machine_id": machine_id,
                    "maintenance_type_id": 1,
                    "related_failure_id": None,
                    "start_time": next_time,
                    "duration_minutes": duration,
                    "technician_id": np.random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10]),
                }
            )

            machine_maintenance.append(
                {"start_time": next_time, "duration_minutes": duration}
            )

    preventive_short = pd.DataFrame(preventive_short)

    # =========================
    # LONG PREVENTIVE (3–6 měsíců)
    # =========================
    preventive_long = []

    for _, machine in machines_df.iterrows():

        machine_id = machine["machine_id"]
        line_id = machine["line_id"]

        machine_maintenance = []

        machine_failures = failures_df[failures_df["machine_id"] == machine_id]

        current_day = time_df["timestamp"].min().normalize()
        end_time_limit = time_df["timestamp"].max()

        attempts = 0

        while True:

            attempts += 1
            if attempts > 100:
                break

            current_day += pd.Timedelta(days=np.random.randint(90, 180))

            next_time = pd.Timestamp(
                year=current_day.year,
                month=current_day.month,
                day=current_day.day,
                hour=np.random.randint(6, 22),
                minute=np.random.randint(0, 60),
            )

            if next_time > end_time_limit:
                break

            duration = np.random.randint(120, 480)

            # ===== KOLIZE S PORUCHOU =====
            collision = machine_failures[
                (machine_failures["failure_time"] - pd.Timedelta(hours=6) <= next_time)
                & (
                    machine_failures["repair_end_time"] + pd.Timedelta(hours=6)
                    >= next_time
                )
            ]

            if not collision.empty:
                continue

            # ===== KOLIZE S EXISTUJÍCÍ MAINTENANCE =====
            overlap = False

            for m in machine_maintenance:

                m_start = m["start_time"]
                m_end = m_start + pd.Timedelta(minutes=m["duration_minutes"])

                new_end = next_time + pd.Timedelta(minutes=duration)

                if (next_time < m_end) and (new_end > m_start):
                    overlap = True
                    break

            if overlap:
                continue

            tech = np.random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])

            if np.random.random() < 0.05:
                tech = 11
            # ==========================================

            preventive_long.append(
                {
                    "line_id": line_id,
                    "machine_id": machine_id,
                    "maintenance_type_id": 1,
                    "related_failure_id": None,
                    "start_time": next_time,
                    "duration_minutes": duration,
                    "technician_id": tech,
                }
            )

            machine_maintenance.append(
                {"start_time": next_time, "duration_minutes": duration}
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

    maintenance["start_time"] = pd.to_datetime(
        maintenance["start_time"], errors="coerce"
    )

    maintenance["end_time"] = pd.to_datetime(maintenance["end_time"], errors="coerce")

    # =========================
    # MAINTENANCE ID
    # =========================

    maintenance = maintenance.sort_values("start_time")
    maintenance = maintenance.reset_index(drop=True)

    maintenance.insert(0, "maintenance_id", range(1, len(maintenance) + 1))

    return maintenance"""

import pandas as pd
import numpy as np


def generate_maintenance(failures_df, machines_df, time_df):

    # =========================
    # REACTIVE MAINTENANCE
    # =========================
    reactive = failures_df.copy()

    reactive["maintenance_type_id"] = 2
    reactive["start_time"] = reactive["repair_start_time"]
    reactive["end_time"] = reactive["repair_end_time"]
    reactive["duration_minutes"] = reactive["repair_time_minutes"]
    reactive["related_failure_id"] = reactive["failure_id"]

    reactive = reactive[
        [
            "machine_id",
            "line_id",
            "maintenance_type_id",
            "related_failure_id",
            "start_time",
            "end_time",
            "duration_minutes",
            "technician_id",
        ]
    ]

    preventive_short = []
    preventive_long = []

    # =========================
    # PREVENTIVE GENERATION
    # =========================
    for _, machine in machines_df.iterrows():

        machine_id = machine["machine_id"]
        line_id = machine["line_id"]

        machine_failures = failures_df[
            failures_df["machine_id"] == machine_id
        ].sort_values("failure_time")

        machine_maintenance = []

        end_time_limit = time_df["timestamp"].max()

        # -------------------------
        # SHORT PREVENTIVE
        # -------------------------
        current_day = time_df["timestamp"].min().normalize()

        attempts = 0

        while True:

            attempts += 1
            if attempts > 100:
                break

            current_day += pd.Timedelta(days=np.random.randint(10, 15))

            next_time = pd.Timestamp(
                year=current_day.year,
                month=current_day.month,
                day=current_day.day,
                hour=np.random.randint(6, 22),
                minute=np.random.randint(0, 60),
            )

            if next_time > end_time_limit:
                break

            duration = np.random.randint(20, 60)

            # ===== KOLIZE S PORUCHOU =====
            collision = machine_failures[
                (machine_failures["failure_time"] - pd.Timedelta(hours=6) <= next_time)
                & (
                    machine_failures["repair_end_time"] + pd.Timedelta(hours=6)
                    >= next_time
                )
            ]

            if not collision.empty:
                continue

            # ===== KOLIZE S EXISTUJÍCÍ MAINTENANCE =====
            overlap = False

            for m in machine_maintenance:

                m_start = m["start_time"]
                m_end = m_start + pd.Timedelta(minutes=m["duration_minutes"])

                new_end = next_time + pd.Timedelta(minutes=duration)

                if (next_time < m_end) and (new_end > m_start):
                    overlap = True
                    break

            if overlap:
                continue

            preventive_short.append(
                {
                    "line_id": line_id,
                    "machine_id": machine_id,
                    "maintenance_type_id": 1,
                    "related_failure_id": None,
                    "start_time": next_time,
                    "duration_minutes": duration,
                    "technician_id": np.random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10]),
                }
            )

            machine_maintenance.append(
                {"start_time": next_time, "duration_minutes": duration}
            )

        # -------------------------
        # LONG PREVENTIVE
        # -------------------------
        current_day = time_df["timestamp"].min().normalize()

        attempts = 0

        while True:

            attempts += 1
            if attempts > 100:
                break

            current_day += pd.Timedelta(days=np.random.randint(90, 180))

            next_time = pd.Timestamp(
                year=current_day.year,
                month=current_day.month,
                day=current_day.day,
                hour=np.random.randint(6, 22),
                minute=np.random.randint(0, 60),
            )

            if next_time > end_time_limit:
                break

            duration = np.random.randint(120, 480)

            # ===== KOLIZE S PORUCHOU =====
            collision = machine_failures[
                (machine_failures["failure_time"] - pd.Timedelta(hours=6) <= next_time)
                & (
                    machine_failures["repair_end_time"] + pd.Timedelta(hours=6)
                    >= next_time
                )
            ]

            if not collision.empty:
                continue

            # ===== KOLIZE S EXISTUJÍCÍ MAINTENANCE =====
            overlap = False

            for m in machine_maintenance:

                m_start = m["start_time"]
                m_end = m_start + pd.Timedelta(minutes=m["duration_minutes"])

                new_end = next_time + pd.Timedelta(minutes=duration)

                if (next_time < m_end) and (new_end > m_start):
                    overlap = True
                    break

            if overlap:
                continue

            tech = np.random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])

            if np.random.random() < 0.05:
                tech = 11

            preventive_long.append(
                {
                    "line_id": line_id,
                    "machine_id": machine_id,
                    "maintenance_type_id": 1,
                    "related_failure_id": None,
                    "start_time": next_time,
                    "duration_minutes": duration,
                    "technician_id": tech,
                }
            )

            machine_maintenance.append(
                {"start_time": next_time, "duration_minutes": duration}
            )

    preventive_short = pd.DataFrame(preventive_short)
    preventive_long = pd.DataFrame(preventive_long)

    # =========================
    # SPOJENÍ
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

    maintenance["start_time"] = pd.to_datetime(
        maintenance["start_time"], errors="coerce"
    )

    maintenance["end_time"] = pd.to_datetime(maintenance["end_time"], errors="coerce")

    # =========================
    # MAINTENANCE ID
    # =========================
    maintenance = maintenance.sort_values("start_time")
    maintenance = maintenance.reset_index(drop=True)

    maintenance.insert(0, "maintenance_id", range(1, len(maintenance) + 1))

    return maintenance


##############################################################################################################################################################################


def add_labor_and_parts(maintenance, technicians_df, spare_parts_df):

    maintenance = maintenance.copy()

    # ======================
    # LABOR COST
    # ======================

    tech_rates = technicians_df.set_index("technician_id")["hourly_rate"]

    maintenance["hourly_rate"] = maintenance["technician_id"].map(tech_rates)

    maintenance["labor_cost"] = (
        maintenance["hourly_rate"] * (maintenance["duration_minutes"] / 60)
    ).round(2)

    maintenance.drop(columns=["hourly_rate"], inplace=True)

    # ======================
    # PARTS
    # ======================

    part_ids = spare_parts_df["part_id"].values
    part_prices = spare_parts_df.set_index("part_id")["cost_per_unit"]

    part_id_list = []
    part_qty_list = []
    part_cost_list = []

    for _, row in maintenance.iterrows():

        mtype = row["maintenance_type_id"]

        # pravděpodobnost použití dílu
        if mtype == 2:  # reactive
            use_part = np.random.random() < 0.7
        else:
            if row["duration_minutes"] >= 120:  # long preventive
                use_part = np.random.random() < 0.6
            else:  # short preventive
                use_part = np.random.random() < 0.3

        if not use_part:
            part_id_list.append(None)
            part_qty_list.append(0)
            part_cost_list.append(0)
            continue

        part_id = np.random.choice(part_ids)

        qty = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])

        cost = part_prices[part_id] * qty

        part_id_list.append(part_id)
        part_qty_list.append(qty)
        part_cost_list.append(cost)

    maintenance["part_id"] = part_id_list
    maintenance["part_quantity"] = part_qty_list
    maintenance["parts_cost"] = part_cost_list

    maintenance["part_id"] = maintenance["part_id"].astype("Int64")
    maintenance["part_quantity"] = maintenance["part_quantity"].astype("Int64")

    return maintenance
