# leakage fixtures: answer key

`leaky/` has 8 planted leaks. `clean/` has the same three pipelines with every leak fixed, and an
audit of it should report 0 findings. Nothing here runs: the data files don't exist. The fixtures
are for static review only.

| # | Location | Class | What leaks |
| --- | --- | --- | --- |
| 1 | `leaky/churn_model.py:12` | target leakage | `city_churn_rate` is the mean of the label per city, computed on all rows, test included |
| 2 | `leaky/churn_model.py:18` | target leakage | `refund_amount_after_cancel` only exists after the customer churned (post-outcome feature) |
| 3 | `leaky/churn_model.py:25` | preprocessing fit on full data | `StandardScaler.fit_transform` runs before the split, so test rows set the mean and variance |
| 4 | `leaky/churn_model.py:34` | train/test contamination | `C` is chosen by test AUC, so the reported test score is a selection on the test set |
| 5 | `leaky/demand_forecast.py:14` | temporal leakage | `rolling(7, center=True)` averages the next 3 days into today's feature |
| 6 | `leaky/demand_forecast.py:19` | temporal leakage | `train_test_split` shuffles a time series, so the model trains on days after the ones it is tested on |
| 7 | `leaky/fraud_spark.py:15` | preprocessing fit on full data | `Imputer(...).fit(tx)` runs before `randomSplit`, so imputation statistics include test rows |
| 8 | `leaky/fraud_spark.py:18` | train/test contamination | a row-level `randomSplit` on transactions with a card-level label puts the same card in train and test |

How `clean/` fixes each leak:

1. and 3. Target encoding and scaling run inside a `Pipeline`, fit on the training split
   (`TargetEncoder` cross-fits).
2. The post-outcome column is dropped.
4. `C` is chosen by `GridSearchCV` on the training split, and the test set is scored once.
5. A past-only window: `shift(1).rolling(7)`.
6. A time-based cutoff, with a one-day gap for the next-day target.
7. and 8. The split is by `card_id`, and the `Imputer` is a pipeline stage fit on train.
