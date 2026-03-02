import pandas as pd
import numpy as np

# Nastavení náhodného semene (aby byla data reprodukovatelná)
np.random.seed(42)

# Počet řádků
n = 20

# Vytvoření jednoduchého datasetu
data = {
    "Machine_ID": np.random.choice(["L1_M1", "L1_M2", "L2_M1"], size=n),
    "Temperature": np.random.normal(loc=70, scale=5, size=n),
    "Vibration": np.random.normal(loc=3, scale=0.5, size=n),
    "Failure": np.random.choice([0, 1], size=n, p=[0.8, 0.2])
}

df = pd.DataFrame(data)

# Uložení do CSV ve stejné složce
df.to_csv("test_data.csv", index=False)

print("Data byla úspěšně vygenerována a uložena jako test_data.csv")
print(df.head())
