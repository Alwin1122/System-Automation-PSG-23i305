
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score
)


df = pd.read_csv(
    r"C:\Users\23i305\Downloads\System-Automation-PSG-23i305\Day2\data\day2_sample.csv"
)


X = df.drop("state", axis=1)
y = df["state"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)


model.fit(X_train, y_train)


y_pred = model.predict(X_test)


print(f"Accuracy:{ accuracy_score(y_test, y_pred):.2%}")

