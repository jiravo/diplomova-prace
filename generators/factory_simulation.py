import numpy as np
import pandas as pd


# =====================================================
# INITIAL MACHINE STATES
# =====================================================


def initialize_machine_states(machines):

    states = []

    for _, row in machines.iterrows():

        rng = np.random.default_rng(abs(hash(row["machine_id"])) % (2**32))

        states.append(
            {
                "machine_id": row["machine_id"],
                "line_id": row["line_id"],
                "rng": rng,
                "health": 1.0,
                "base_degradation": rng.uniform(0.00015, 0.00035),
                "failure_threshold": rng.uniform(0.45, 0.6),
                "is_running": True,
                "hours_since_maintenance": 0,
                "failure_remaining_hours": 0,
            }
        )

    return states


# =====================================================
# MACHINE BEHAVIOUR PER HOUR
# =====================================================


def simulate_hour(state):

    # -----------------------------
    # MACHINE FAILURE ACTIVE
    # -----------------------------
    if state["failure_remaining_hours"] > 0:

        state["is_running"] = False
        state["failure_remaining_hours"] -= 1

        # porucha skončila → oprava
        if state["failure_remaining_hours"] == 0:

            recovery = state["rng"].uniform(0.25, 0.5)

            state["health"] = min(1.0, state["health"] + recovery)

            state["hours_since_maintenance"] = 0

    else:
        state["is_running"] = True

        # -----------------------------
        # NORMAL DEGRADATION
        # -----------------------------
        degradation = state["base_degradation"] * state["rng"].uniform(0.8, 1.2)

        state["health"] -= degradation
        state["health"] = max(state["health"], 0.05)

        state["hours_since_maintenance"] += 1

    return state


# =====================================================
# SENSOR GENERATION
# =====================================================


def generate_sensor_values(state, timestamp):

    health = state["health"]
    rng = state["rng"]

    # ==================================
    # AMBIENT TEMPERATURE (FACTORY HALL)
    # ==================================

    day_of_year = timestamp.timetuple().tm_yday

    # venkovní sezónnost (-5 až 30)
    outside_temp = 12 + 18 * np.sin((day_of_year - 80) / 365 * 2 * np.pi)

    # hala tlumí vlivy prostředí
    ambient_temperature = (
        20  # základ haly
        + 0.25 * outside_temp  # jen část vlivu venku
        + rng.normal(0, 0.8)  # malé kolísání
    )

    # bezpečné limity haly
    ambient_temperature = np.clip(ambient_temperature, 15, 30)

    temperature = ambient_temperature + 30 + (1 - health) * 40 + rng.normal(0, 2)
    vibration = 2 + (1 - health) * 5 + rng.normal(0, 0.3)
    pressure = 5 + (1 - health) * 2 + rng.normal(0, 0.2)
    load = rng.uniform(60, 90)

    # bezpečné limity
    temperature = np.clip(temperature, 20, 120)
    vibration = np.clip(vibration, 0, 10)
    pressure = np.clip(pressure, 1, 10)
    load = np.clip(load, 0, 100)

    if state["is_running"]:
        produced_units = int(rng.normal(80 * state["health"], 5))
    else:
        produced_units = 0

    produced_units = max(produced_units, 0)

    return {
        "temperature": temperature,
        "vibration": vibration,
        "pressure": pressure,
        "load": load,
        "ambient_temperature": ambient_temperature,
        "produced_units": produced_units,
    }


# =====================================================
# FAILURE CHECK
# =====================================================


def check_failure(state):

    if state["health"] < state["failure_threshold"]:

        # pravděpodobnost roste s degradací
        probability = (1 - state["health"]) * 0.15

        if state["rng"].random() < probability:

            duration = state["rng"].integers(2, 12)

            state["failure_remaining_hours"] = duration

            # porucha zhorší stav,
            # ale zařízení nezničí
            state["health"] *= state["rng"].uniform(0.7, 0.85)

            return True, duration

    return False, 0


# =====================================================
# MAIN FACTORY SIMULATION
# =====================================================


def run_factory_simulation(machines, time_df):

    states = initialize_machine_states(machines)

    sensor_rows = []
    failures = []

    for _, time_row in time_df.iterrows():

        timestamp = time_row["timestamp"]
        shift_id = time_row["shift_id"]

        for state in states:

            state = simulate_hour(state)

            failure_started, duration = check_failure(state)

            sensors = generate_sensor_values(state, timestamp)

            # ---------------- SENSOR DATA ----------------
            sensor_rows.append(
                {
                    "timestamp": timestamp,
                    "machine_id": state["machine_id"],
                    "line_id": state["line_id"],
                    "shift_id": shift_id,
                    "is_running": int(state["is_running"]),
                    "temperature": sensors["temperature"],
                    "vibration": sensors["vibration"],
                    "pressure": sensors["pressure"],
                    "load": sensors["load"],
                    "ambient_temperature": sensors["ambient_temperature"],
                    "produced_units": sensors["produced_units"],
                    "operating_hours_since_maintenance": state[
                        "hours_since_maintenance"
                    ],
                    "health_index": state["health"],
                }
            )

            # ---------------- FAILURE LOG ----------------
            if failure_started:

                failures.append(
                    {
                        "machine_id": state["machine_id"],
                        "line_id": state["line_id"],
                        "failure_time": timestamp,
                        "downtime_hours": duration,
                    }
                )

    sensor_df = pd.DataFrame(sensor_rows)
    failures_df = pd.DataFrame(failures)

    return sensor_df, failures_df
