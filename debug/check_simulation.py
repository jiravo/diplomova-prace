import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/Source/sensor_data.csv")

# timestamp MUSÍ být datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# vyber jeden stroj
df_machine = df[df["machine_id"] == "M1"]

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

m = df[df.machine_id == "M1"]

plt.plot(m["health_index"])
plt.scatter(
    failures[failures.machine_id == "M1"]["failure_time"],
    [0.4] * len(failures[failures.machine_id == "M1"]),
    color="red",
)
plt.show()


print("#############################")
