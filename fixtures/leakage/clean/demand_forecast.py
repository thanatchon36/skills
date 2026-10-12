"""Forecast next-day store demand from daily sales history."""

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

sales = pd.read_csv("data/daily_sales.csv", parse_dates=["date"])
sales = sales.sort_values(["store_id", "date"])

sales["target"] = sales.groupby("store_id")["units"].shift(-1)
sales["units_lag_1"] = sales.groupby("store_id")["units"].shift(1)
sales["units_avg_7d"] = sales.groupby("store_id")["units"].transform(
    lambda s: s.shift(1).rolling(7, min_periods=1).mean()
)
sales = sales.dropna(subset=["target", "units_lag_1"])

features = ["units_lag_1", "units_avg_7d", "promo", "day_of_week"]
cutoff = sales["date"].quantile(0.8)
train = sales[sales["date"] < cutoff - pd.Timedelta(days=1)]
test = sales[sales["date"] >= cutoff]

model = GradientBoostingRegressor(random_state=0).fit(train[features], train["target"])
print("MAE", mean_absolute_error(test["target"], model.predict(test[features])))
