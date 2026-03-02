import numpy as np

SEED = 42
rng = np.random.default_rng(SEED)

# čas
START_DATE = "2022-01-01"
END_DATE = "2024-12-31"
FREQ = "1h"

# výroba
NUM_LINES = 3
MACHINES_PER_LINE = 4

# poruchovost
FAILURE_INTERVAL_WEEKS_MIN = 3
FAILURE_INTERVAL_WEEKS_MAX = 5

# health model
INITIAL_HEALTH = 1.0
DEGRADATION_RATE = 0.00003

# maintenance efekty
PREVENTIVE_HEALTH_BOOST = (0.05, 0.15)
REPAIR_HEALTH_RESET = (0.75, 0.9)
