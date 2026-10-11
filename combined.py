
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv(
    r"C:\Users\23i305\Downloads\System-Automation-PSG-23i305\Day2\data\day2_sample.csv"
)

X = df.drop("state", axis=1)
y = df["state"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=100, random_state=42, class_weight="balanced"
)
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))

MACHINES = ["Machine_A", "Machine_B", "Machine_C"]

RULES = [
    (1, "Critical overload", "current", 28, "Cut power"),
    (2, "High temperature", "temperature", 85, "Stop machine"),
    (3, "High pressure", "pressure", 45, "Vent pressure")
]

def generate_data():
    readings = {}

    for machine in MACHINES:
        readings[machine] = {
            "temperature": random.uniform(50, 100),
            "pressure": random.uniform(20, 55),
            "vibration": random.uniform(0.5, 4),
            "current": random.uniform(5, 35),
            "rpm": random.randint(1000, 3000)
        }

    return readings

def analyze_data(readings, log):
    incidents = []

    for machine, data in readings.items():
        prediction = model.predict(pd.DataFrame([data]))[0]

        log.append(f"\n{machine}: {data}")
        log.append(f"Predicted State: {prediction}")

        for priority, name, sensor, limit, action in RULES:
            if data[sensor] > limit:
                incidents.append(
                    (priority, machine, name, action)
                )
                break

    return sorted(incidents)

def main():
    log = []

    log.append("Monitor")
    log.append(f"Model Accuracy: {accuracy:.2%}")

    readings = generate_data()
    incidents = analyze_data(readings, log)

    if incidents:
        log.append("\nIncident")

        for priority, machine, reason, action in incidents:
            log.append(
                f"{machine} | Priority {priority} | "
                f"{reason} | Action: {action}"
            )

        log.append("\nDashboard")
        log.append(f"Machines monitored: {len(MACHINES)}")
        log.append(f"Active incidents: {len(incidents)}")
        log.append(f"Highest priority: {incidents[0][2]}")

    else:
        log.append("\nAll machines are operating normally.")
        log.append("Active incidents: 0")

    log.append("\nSecurity Validation")

    for machine, data in readings.items():
        if any(value < 0 for value in data.values()):
            log.append(f"Invalid sensor data detected: {machine}")
        else:
            log.append(f"{machine}: Sensor data valid")

    log.append("\nMonitoring complete.")


    with open("factory_monitor_log.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(log))

    print("\n".join(log))
    

if __name__ == "__main__":
    main()