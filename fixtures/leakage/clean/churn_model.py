"""Train a churn classifier on the customer snapshot table."""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, TargetEncoder

df = pd.read_parquet("data/customers.parquet")

numeric = ["tenure_months", "monthly_spend", "support_tickets_90d"]
categorical = ["city"]
X = df[numeric + categorical]
y = df["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

preprocess = ColumnTransformer(
    [
        ("num", StandardScaler(), numeric),
        ("city", TargetEncoder(target_type="binary"), categorical),
    ]
)
pipeline = Pipeline([("prep", preprocess), ("clf", LogisticRegression(max_iter=1000))])

search = GridSearchCV(pipeline, {"clf__C": [0.01, 0.1, 1.0, 10.0]}, scoring="roc_auc", cv=5)
search.fit(X_train.fillna(0), y_train)

test_auc = roc_auc_score(y_test, search.predict_proba(X_test.fillna(0))[:, 1])
print(f"best C={search.best_params_['clf__C']} test AUC={test_auc:.3f}")
