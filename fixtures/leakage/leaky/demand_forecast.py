"""Forecast next-day store demand from daily sales history."""

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

sales = pd.read_csv("data/daily_sales.csv", parse_dates=["date"])
sales = sales.sort_values(["store_id", "date"])

sales["target"] = sales.groupby("store_id")["units"].shift(-1)
sales["units_lag_1"] = sales.groupby("store_id")["units"].shift(1)
sales["units_avg_7d"] = sales.groupby("store_id")["units"].transform(
    lambda s: s.rolling(7, center=True, min_periods=1).mean()
)
sales = sales.dropna(subset=["target", "units_lag_1"])

features = ["units_lag_1", "units_avg_7d", "promo", "day_of_week"]
X_train, X_test, y_train, y_test = train_test_split(
    sales[features], sales["target"], test_size=0.2, random_state=0
)

model = GradientBoostingRegressor(random_state=0).fit(X_train, y_train)
print("MAE", mean_absolute_error(y_test, model.predict(X_test)))
