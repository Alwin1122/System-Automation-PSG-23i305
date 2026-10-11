from pathlib import Path
import numpy as np
import pandas as pd

# Set reproducible seed
np.random.seed(42)

# Define states and ensure perfectly even distribution
# Using 240 samples gives exactly 60 samples per state (240 / 4 = 60),
# and exactly 20 samples per failure rule (60 / 3 = 20)
state_names = ["Normal", "Warning", "Failure", "Off"]
samples_per_state = 60
n_samples = samples_per_state * len(state_names)  # 240 samples

times = pd.date_range("2026-10-11 12:00:00", periods=n_samples, freq="1s")

# Distribute states evenly
states = np.array(
    ["Normal"] * samples_per_state +
    ["Warning"] * samples_per_state +
    ["Failure"] * samples_per_state +
    ["Off"] * samples_per_state
)

# Evenly distribute failure modes across the failure samples
failure_rules = ["temp", "pressure", "vibration"]
rules_per_type = samples_per_state // len(failure_rules)  # 20 each
failure_mode_allocation = np.array(
    ["temp"] * rules_per_type +
    ["pressure"] * rules_per_type +
    ["vibration"] * rules_per_type
)
np.random.shuffle(failure_mode_allocation)

# Shuffle states across time
permutation = np.random.permutation(n_samples)
states = states[permutation]

temp = np.zeros(n_samples)
rpm = np.zeros(n_samples)
press = np.zeros(n_samples)
vib = np.zeros(n_samples)
current = np.zeros(n_samples)

failure_idx = 0
for i, state in enumerate(states):
    # Baseline nominal operating ranges
    temp[i] = np.random.uniform(40, 80)
    rpm[i] = np.random.uniform(1200, 2200)
    press[i] = np.random.uniform(1.5, 4.5)
    vib[i] = np.random.uniform(0.5, 3.5)
    current[i] = np.random.uniform(8.0, 15.0)

    if state == "Warning":
        # Elevated temperature warning zone
        temp[i] = np.random.uniform(80.5, 89.5)

    elif state == "Failure":
        # Multi-rule failure: evenly distributed rule violations
        rule = failure_mode_allocation[failure_idx]
        failure_idx += 1
        
        if rule == "temp":
            temp[i] = np.random.uniform(90.1, 98.0)
        elif rule == "pressure":
            press[i] = np.random.uniform(6.1, 8.0)
        else:
            vib[i] = np.random.uniform(5.5, 9.5)

    elif state == "Off":
        # When machine is powered down
        rpm[i] = 0.0
        current[i] = 0.0
        vib[i] = 0.0
        press[i] = 1.0  # Atmospheric pressure
        temp[i] = np.random.uniform(22.0, 26.0)  # Ambient room temperature

data = {
    "Timestamp": times,
    "State": states,
    "Temperature_C": np.round(temp, 1),
    "Pressure_Bar": np.round(press, 1),
    "Vibration_g": np.round(vib, 1),
    "RPM": np.round(rpm, 0),
    "Current_Amps": np.round(current, 1),
}

df = pd.DataFrame(data)

output_path = Path(__file__).resolve().parent / "multi_rule_sensor_data.csv"
df.to_csv(output_path, index=False)
print(f"Generated {len(df)} evenly distributed samples saved to: {output_path}")
print("State distribution:\n", df["State"].value_counts())
