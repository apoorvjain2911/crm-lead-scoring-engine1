import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# -----------------------------
# 1. Sample CRM dataset
# -----------------------------
data = pd.DataFrame([
    [120, "SaaS", 8, 14, 1, "LinkedIn", 1],
    [50, "E-commerce", 2, 3, 0, "Google Ads", 0],
    [300, "Fintech", 10, 20, 1, "Referral", 1],
    [30, "EdTech", 1, 2, 0, "Organic", 0],
    [200, "SaaS", 7, 10, 1, "LinkedIn", 1],
    [80, "Healthcare", 3, 5, 0, "Cold Email", 0],
])

data.columns = [
    "company_size",
    "industry",
    "email_opens",
    "website_visits",
    "demo_requested",
    "lead_source",
    "converted"
]

# -----------------------------
# 2. Split data
# -----------------------------
X = data.drop("converted", axis=1)
y = data["converted"]

categorical = ["industry", "lead_source"]
numerical = ["company_size", "email_opens", "website_visits", "demo_requested"]

# -----------------------------
# 3. Preprocessing pipeline
# -----------------------------
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numerical),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical)
])

# -----------------------------
# 4. Model pipeline
# -----------------------------
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression())
])

# -----------------------------
# 5. Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 6. Train model
# -----------------------------
model.fit(X_train, y_train)

# -----------------------------
# 7. Evaluate model
# -----------------------------
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)

print("Accuracy:", acc)

# -----------------------------
# 8. Save model
# -----------------------------
joblib.dump(model, "lead_scoring_model.pkl")

print("Model saved successfully!")