import random
import time


MACHINES = ["machine_A", "machine_B", "machine_C", "machine_D", "machine_E"]


RULES = [
    {"name": "critical overload", "priority": 1, "condition": lambda r: r["current"] is not None and r["current"] > 28, "action": "cut power"},
    {"name": "high temp",         "priority": 2, "condition": lambda r: r["temperature"] is not None and r["temperature"] > 85, "action": "stop machine"},
    {"name": "high pressure",     "priority": 3, "condition": lambda r: r["pressure"] is not None and r["pressure"] > 45, "action": "vent pressure"},
]



def generate_factory_data():
    factory_snapshot = {}
    for m in MACHINES:

        spike = random.random() < 0.05
        factory_snapshot[m] = {
            "temperature": random.uniform(90, 100) if spike else random.uniform(50, 80),
            "pressure":    random.uniform(46, 55)  if spike else random.uniform(20, 40),
            "current":     random.uniform(29, 35)  if spike else random.uniform(5, 20)
        }
    return factory_snapshot



def analyze_factory(factory_data):
    incidents = []
    
    for machine_id, reading in factory_data.items():
    
        for rule in sorted(RULES, key=lambda x: x["priority"]):
            if rule["condition"](reading):
                incidents.append({
                    "machine": machine_id,
                    "rule_name": rule["name"],
                    "priority": rule["priority"],
                    "action": rule["action"]
                })
                break 
                
    
    incidents.sort(key=lambda x: x["priority"])
    return incidents


def main():
    print("--- Factory Monitor ---\n")
    

    current_snapshot = generate_factory_data()
    active_issues = analyze_factory(current_snapshot)
    
  
    if active_issues:
        primary_threat = active_issues[0]
        print(f"   immediate response: {primary_threat['machine']}")
        print(f"   Reason: {primary_threat['rule_name']}")
        print(f"   Action: {primary_threat['action']}\n")

        
        print("Full Incident Queue:")
        for issue in active_issues:
            print(f" - [{issue['machine']}] Priority {issue['priority']} -> {issue['rule_name']} ({issue['action']})")

    else:
        print("No machines require immediate response.")



if __name__ == "__main__":
    main()
