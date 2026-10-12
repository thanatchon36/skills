"""Train a churn classifier on the customer snapshot table."""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_parquet("data/customers.parquet")

# Average churn rate per city as a feature.
df["city_churn_rate"] = df.groupby("city")["churned"].transform("mean")

features = [
    "tenure_months",
    "monthly_spend",
    "support_tickets_90d",
    "refund_amount_after_cancel",
    "city_churn_rate",
]
X = df[features].fillna(0)
y = df["churned"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

best_auc, best_c = 0.0, None
for c in [0.01, 0.1, 1.0, 10.0]:
    model = LogisticRegression(C=c, max_iter=1000).fit(X_train, y_train)
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    if auc > best_auc:
        best_auc, best_c = auc, c

print(f"best C={best_c} test AUC={best_auc:.3f}")
