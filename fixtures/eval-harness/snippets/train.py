import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("loans.csv")
X, y = df.drop(columns=["default"]), df["default"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, stratify=y)

model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
pred = model.predict(X_test)
print(f"accuracy: {accuracy_score(y_test, pred):.3f}")
