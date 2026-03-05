import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/Source/sensor_data.csv")

# timestamp MUSÍ být datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# vyber jeden stroj
df_machine = df[df["machine_id"] == 1]

# menší časové okno (např. 10 dní)
df_machine = df_machine.iloc[:240]

m = df_machine

# =========================
# TEMPERATURE
# =========================
plt.figure(figsize=(12, 5))
plt.plot(m["timestamp"], m["temperature"])
plt.title("Temperature trend")
plt.xticks(rotation=45)
plt.show()

# =========================
# VIBRATION
# =========================
plt.figure(figsize=(12, 5))
plt.plot(m["timestamp"], m["vibration"])
plt.title("Vibration trend")
plt.xticks(rotation=45)
plt.show()

# =========================
# HEALTH
# =========================
plt.figure(figsize=(12, 5))
plt.plot(m["timestamp"], m["health_index"])
plt.title("Health index")
plt.xticks(rotation=45)
plt.show()

# =========================
# AMBIENT
# =========================
plt.figure(figsize=(12, 5))
plt.plot(m["timestamp"], m["ambient_temperature"])
plt.title("Ambient temperature")
plt.xticks(rotation=45)
plt.show()


failures = pd.read_csv("data/Source/failures.csv")

print(failures.groupby("machine_id").size())

print(df["machine_id"].unique())

print("#############################")

print(df[["health_index", "temperature", "vibration", "pressure"]].corr())

print("#############################")

m = df[df.machine_id == 1]

plt.plot(m["health_index"])
plt.scatter(
    failures[failures.machine_id == 1]["failure_time"],
    [0.4] * len(failures[failures.machine_id == 1]),
    color="red",
)
plt.show()


print("#############################")
print(failures["failure_type"].value_counts())
print(failures["failure_type"].value_counts(normalize=True))
print(failures.groupby("machine_id").size().sort_values(ascending=False))

machines = pd.read_csv("data/BI/D_Machine.csv")
failures = pd.read_csv("data/Source/failures.csv")

# spojení přes machine_id
merged = failures.merge(
    machines[["machine_id", "machine_type_id"]], on="machine_id", how="left"
)

print(merged.groupby(["machine_type_id", "failure_type"]).size())

df_line = df[(df["line_id"] == 1) & (df["timestamp"] == "2024-10-24 11:00:00")]

print(df_line[["machine_id", "is_running", "produced_units"]])

print("###########################################")

import pandas as pd

df = pd.read_csv("data/Source/sensor_data.csv")
failures = pd.read_csv("data/Source/failures.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])
failures["failure_time"] = pd.to_datetime(failures["failure_time"])

# najdeme poruchu, která není na poslední stanici
test_failure = None

for _, f in failures.iterrows():
    if f["machine_id"] not in [4, 8, 12]:  # poslední stanice linek
        test_failure = f
        break

print("Testujeme poruchu:")
print(test_failure)

snapshot = df[
    (df["line_id"] == test_failure["line_id"])
    & (df["timestamp"] == test_failure["failure_time"])
].sort_values("machine_id")

print("\nStav linky v daný čas:")
print(snapshot[["machine_id", "is_running", "produced_units"]])

import pandas as pd

failures = pd.read_csv("data/Source/failures.csv")

print(failures["machine_id"].value_counts().sort_index())


print("##############")

print(df[(df["is_running"] == 0) & (df["produced_units"] > 0)])


print(failures["severity_id"].value_counts())


print(
    failures[failures["failure_type"] == "electrical"]["technician_id"].value_counts()
)


maintenance = pd.read_csv("data/Source/maintenance.csv")

print(maintenance["maintenance_type_id"].value_counts())


print(maintenance.dtypes)

maintenance = pd.read_csv("data/Source/maintenance.csv")

maintenance["start_time"] = pd.to_datetime(maintenance["start_time"])

print(
    maintenance[
        (maintenance["maintenance_type_id"] == 1)
        & (
            (maintenance["start_time"].dt.hour < 6)
            | (maintenance["start_time"].dt.hour >= 22)
        )
    ]
)


maintenance = pd.read_csv("data/Source/maintenance.csv")

long_pm = maintenance[
    (maintenance["maintenance_type_id"] == 1) & (maintenance["duration_minutes"] >= 120)
]

print(long_pm.groupby("machine_id").size())

print(maintenance.dtypes)

parts = pd.read_csv("data/BI/D_SparePart.csv")
maintenance = pd.read_csv("data/Source/maintenance.csv")

invalid = maintenance[
    ~maintenance["part_id"].isin(parts["part_id"]) & maintenance["part_id"].notna()
]

print(invalid)
