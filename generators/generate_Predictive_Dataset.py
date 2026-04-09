import pandas as pd
import numpy as np

# ===============================
# LOAD DATA
# ===============================

sensor = pd.read_csv("data/Source/sensor_data.csv", parse_dates=["timestamp"])

failures = pd.read_csv("data/Source/failures.csv", parse_dates=["failure_time"])

print("Sensor shape:", sensor.shape)
print("Failures shape:", failures.shape)

# ===============================
# SORT DATA
# ===============================

sensor = sensor.sort_values(["machine_id", "timestamp"])
sensor = sensor.reset_index(drop=True)

print(sensor.head())
print(sensor.dtypes)

# ===============================
# BASE ML DATASET
# ===============================

ml_df = sensor[
    [
        "timestamp",
        "machine_id",
        "temperature",
        "vibration",
        "pressure",
        "load",
        "ambient_temperature",
        "is_running",
        "produced_units",
        "defective_units",
        "operating_hours_since_maintenance",
        "machine_age_hours",
        "health_index",
    ]
].copy()

print("ML base dataset:", ml_df.shape)

# ===============================
# SORT DATA
# ===============================

ml_df = ml_df.sort_values(["machine_id", "timestamp"])
ml_df = ml_df.reset_index(drop=True)

print(ml_df.head())
print(ml_df.dtypes)

# ==============================================================================================================================================================================================================
# ZAČÁTEK - PREPROCESSING
# ==============================================================================================================================================================================================================

# ===============================
# HEALTH DELTA 24H
# ===============================

ml_df["health_delta_24h"] = ml_df.groupby("machine_id")["health_index"].diff(24)

print("TVORBA NEW FEATURES")

print(ml_df[["machine_id", "timestamp", "health_index", "health_delta_24h"]].head(30))
print(ml_df["health_delta_24h"].describe())

# ===============================
# ROLLING FEATURES 24H
# ===============================

window = 24

# temperature
ml_df["rolling_temp_mean_24h"] = (
    ml_df.groupby("machine_id")["temperature"]
    .rolling(window)
    .mean()
    .reset_index(level=0, drop=True)
)

ml_df["rolling_temp_std_24h"] = (
    ml_df.groupby("machine_id")["temperature"]
    .rolling(window)
    .std()
    .reset_index(level=0, drop=True)
)

# vibration
ml_df["rolling_vibration_mean_24h"] = (
    ml_df.groupby("machine_id")["vibration"]
    .rolling(window)
    .mean()
    .reset_index(level=0, drop=True)
)

ml_df["rolling_vibration_std_24h"] = (
    ml_df.groupby("machine_id")["vibration"]
    .rolling(window)
    .std()
    .reset_index(level=0, drop=True)
)

# pressure
ml_df["rolling_pressure_mean_24h"] = (
    ml_df.groupby("machine_id")["pressure"]
    .rolling(window)
    .mean()
    .reset_index(level=0, drop=True)
)

ml_df["rolling_pressure_std_24h"] = (
    ml_df.groupby("machine_id")["pressure"]
    .rolling(window)
    .std()
    .reset_index(level=0, drop=True)
)

# KONTROLA

print(ml_df[["temperature", "rolling_temp_mean_24h", "rolling_temp_std_24h"]].head(40))

# ===============================
# RUNNING RATIO 24H
# ===============================

ml_df["running_ratio_24h"] = (
    ml_df.groupby("machine_id")["is_running"]
    .rolling(24)
    .mean()
    .reset_index(level=0, drop=True)
)

# KONTROLA

print(ml_df[["is_running", "running_ratio_24h"]].head(40))
print(ml_df.shape)

# ===============================
# PREPARE FAILURE DATA
# ===============================

failures_small = failures[["machine_id", "failure_time"]].copy()

failures_small = failures_small.sort_values(["machine_id", "failure_time"])

# ===============================
# HOURS SINCE LAST FAILURE
# ===============================

ml_df["hours_since_last_failure"] = np.nan

for machine in ml_df["machine_id"].unique():

    machine_failures = failures_small[failures_small["machine_id"] == machine][
        "failure_time"
    ].values

    last_failure_time = None

    machine_rows = ml_df["machine_id"] == machine

    for idx, row in ml_df[machine_rows].iterrows():

        current_time = row["timestamp"]

        past_failures = machine_failures[machine_failures <= current_time]

        if len(past_failures) == 0:
            continue

        last_failure_time = past_failures[-1]

        diff = current_time - last_failure_time

        ml_df.loc[idx, "hours_since_last_failure"] = diff.total_seconds() / 3600

# KONTROLA

print(ml_df[["timestamp", "machine_id", "hours_since_last_failure"]].dropna().head(20))
print(ml_df["hours_since_last_failure"].describe())
print(ml_df.shape)


# ===================================
# FAILURE COUNT LAST 7 DAYS + 30 DAYS
# ===================================

# 7 DAYS

ml_df["failure_count_last_7d"] = 0

for machine in ml_df["machine_id"].unique():

    machine_failures = failures_small[failures_small["machine_id"] == machine][
        "failure_time"
    ].values

    machine_rows = ml_df["machine_id"] == machine

    for idx, row in ml_df[machine_rows].iterrows():

        current_time = row["timestamp"]

        window_start = current_time - pd.Timedelta(days=7)

        count = np.sum(
            (machine_failures >= window_start) & (machine_failures <= current_time)
        )

        ml_df.loc[idx, "failure_count_last_7d"] = count

# 30 DAYS

ml_df["failure_count_last_30d"] = 0

for machine in ml_df["machine_id"].unique():

    machine_failures = failures_small[failures_small["machine_id"] == machine][
        "failure_time"
    ].values

    machine_rows = ml_df["machine_id"] == machine

    for idx, row in ml_df[machine_rows].iterrows():

        current_time = row["timestamp"]

        window_start = current_time - pd.Timedelta(days=30)

        count = np.sum(
            (machine_failures >= window_start) & (machine_failures <= current_time)
        )

        ml_df.loc[idx, "failure_count_last_30d"] = count

# KONTROLA

print(ml_df["failure_count_last_7d"].value_counts().head())
print(ml_df["failure_count_last_30d"].value_counts().head())


# ==============================================================================================================================================================================================================
# TARGET PROMĚNNÉ
# ==============================================================================================================================================================================================================

# ===============================
# TARGET FAILURE 72H
# ===============================

print("KONTROLA TARGET SLOUPCŮ")

print("FAILURE 72H")

ml_df["target_failure_72h"] = 0

for machine in ml_df["machine_id"].unique():

    machine_failures = failures_small[failures_small["machine_id"] == machine][
        "failure_time"
    ].values

    machine_rows = ml_df["machine_id"] == machine

    for idx, row in ml_df[machine_rows].iterrows():

        current_time = row["timestamp"]

        future_limit = current_time + pd.Timedelta(hours=72)

        future_failures = machine_failures[
            (machine_failures > current_time) & (machine_failures <= future_limit)
        ]

        if len(future_failures) > 0:
            ml_df.loc[idx, "target_failure_72h"] = 1

# KONTROLA

print(ml_df["target_failure_72h"].value_counts())
print(ml_df.shape)

# ===============================
# TARGET FAILURE TYPE
# ===============================

print("FAILURE TYPE")

ml_df["target_failure_type"] = None

for machine in ml_df["machine_id"].unique():

    machine_failures = failures[failures["machine_id"] == machine][
        ["failure_time", "failure_type"]
    ]

    machine_rows = ml_df["machine_id"] == machine

    for idx, row in ml_df[machine_rows].iterrows():

        current_time = row["timestamp"]

        # 👉 jen pokud má nastat porucha do 72h
        if row["target_failure_72h"] != 1:
            continue

        future_failures = machine_failures[
            machine_failures["failure_time"] >= current_time
        ]

        if future_failures.empty:
            continue

        next_failure = future_failures.iloc[0]

        # 🔥 KLÍČOVÁ PODMÍNKA
        if next_failure["failure_time"] <= current_time + pd.Timedelta(hours=72):
            ml_df.loc[idx, "target_failure_type"] = next_failure["failure_type"]

# ===============================
# TARGET RUL HOURS
# ===============================

print("RUL")

ml_df["target_RUL_hours"] = np.nan

for machine in ml_df["machine_id"].unique():

    machine_failures = failures_small[failures_small["machine_id"] == machine][
        "failure_time"
    ].values

    machine_rows = ml_df["machine_id"] == machine

    for idx, row in ml_df[machine_rows].iterrows():

        current_time = row["timestamp"]

        future_failures = machine_failures[machine_failures >= current_time]

        if len(future_failures) == 0:
            continue

        next_failure = future_failures[0]

        diff = next_failure - current_time

        ml_df.loc[idx, "target_RUL_hours"] = diff.total_seconds() / 3600

print(ml_df["target_RUL_hours"].describe())


# ==============================================================================================================================================================================================================
# TESTY
# ==============================================================================================================================================================================================================

# ===============================
# DATA LEAKAGE CHECK
# ===============================

test = ml_df[
    (ml_df["target_failure_72h"] == 1) & (ml_df["hours_since_last_failure"] == 0)
]

print("Rows where model sees failure immediately:", len(test))

# ===============================
# TARGET TIMELINE CHECK
# ===============================

machine = 1

test = ml_df[ml_df["machine_id"] == machine].copy()

failure_times = failures_small[failures_small["machine_id"] == machine]["failure_time"]

f = failure_times.iloc[0]

window = test[
    (test["timestamp"] >= f - pd.Timedelta(hours=100))
    & (test["timestamp"] <= f + pd.Timedelta(hours=10))
]

print(window[["timestamp", "target_failure_72h"]])


# ===============================
# CHECK GRAFEM
# ===============================

import matplotlib.pyplot as plt

machine = 1

m = ml_df[ml_df["machine_id"] == machine].copy()

failure_times = failures[failures["machine_id"] == machine]["failure_time"]

# vyber první poruchu
f = failure_times.iloc[0]

window = m[
    (m["timestamp"] >= f - pd.Timedelta(days=5))
    & (m["timestamp"] <= f + pd.Timedelta(hours=5))
]

plt.figure(figsize=(12, 5))

plt.plot(window["timestamp"], window["health_index"], label="Health index")
plt.plot(window["timestamp"], window["vibration"], label="Vibration")

plt.axvline(f, color="red", linestyle="--", label="Failure")

plt.legend()
plt.xticks(rotation=45)
plt.title("Machine degradation before failure")

plt.show()

print(ml_df.groupby("target_failure_type")["target_RUL_hours"].mean())

# ===============================
# ULOŽENÍ
# ===============================

ml_df.to_csv("data/ML/Predictive_Dataset.csv", index=False)

#################################################################################################################


print("FINÁLNÍ KONTROLA")

import pandas as pd

df = pd.read_csv("data/ML/Predictive_Dataset.csv", parse_dates=["timestamp"])

print("Shape:", df.shape)

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nBasic stats:")
print(df.describe())

print(df["target_failure_72h"].value_counts())

print("\nFailure type distribution:")
print(df["target_failure_type"].value_counts())

print("\nRUL stats:")
print(df["target_RUL_hours"].describe())

print(df.groupby("machine_id")["timestamp"].diff().value_counts().head())

print(df[["health_index", "vibration", "temperature", "target_RUL_hours"]].corr())

print(
    df.groupby("target_failure_72h")[
        ["vibration", "temperature", "health_index"]
    ].mean()
)


print(df.groupby("target_failure_72h")["health_delta_24h"].mean())

#################################################################################################################

print("JEŠTĚ DALŠÍ KONTROLY PRO ML")

print(df["target_failure_72h"].value_counts(normalize=True))

print(df.groupby("machine_id")["target_failure_72h"].mean())

print(failures.groupby("machine_id").size())

###################################################################################################################

"""print("TESTOVACÍ GRAF KDYBY NĚCO")

import pandas as pd
import matplotlib.pyplot as plt

# vybereme jen data před poruchou
df_failure_window = df[(df["target_RUL_hours"] >= 0) & (df["target_RUL_hours"] <= 72)]

# průměrné hodnoty senzorů podle vzdálenosti od poruchy
trend = df_failure_window.groupby("target_RUL_hours")[["vibration", "temperature", "health_index"]].mean()

# vykreslení
plt.figure(figsize=(8,5))

plt.plot(trend.index, trend["vibration"], label="Vibration")
plt.plot(trend.index, trend["temperature"], label="Temperature")
plt.plot(trend.index, trend["health_index"], label="Health index")

plt.gca().invert_xaxis()

plt.xlabel("Hours before failure")
plt.ylabel("Sensor value")
plt.title("Sensor trends before failure")

plt.legend()
plt.show()"""
