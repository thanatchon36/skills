# Leak catalog

Each entry gives the leak, what it looks like in pandas, scikit-learn, and PySpark, the question
that confirms it, and the usual fix. A pattern match alone is never a finding. Answer the
confirming question from the code.

## 1. Target leakage

The model sees information that encodes the label, or that only exists after the outcome.

| Looks like | Confirm |
| --- | --- |
| `df.groupby(k)[target].transform("mean")`, `.agg` over the label, hand-rolled target encoding, `TargetEncoder` fit outside a CV fold | Is the statistic computed on rows that include the row being predicted, or on evaluation rows? |
| Columns named `*_after_*`, `post_*`, `final_*`, `resolved_*`, `refund*`, `chargeback*`, `cancel*`, `outcome*` | Would this value exist at the moment the prediction is made? If the code can't tell you, report it as **suspected** and ask. |
| A feature derived from the label by arithmetic (`label * x`, `days_until_event`) | Does the formula reference the target or the event time? |
| A join to a table keyed by outcome (claims, cancellations, returns) | Is the join filtered to records dated before the prediction time? |

Fix: drop post-outcome columns. Compute target statistics inside the training fold only
(scikit-learn `TargetEncoder` inside a `Pipeline` cross-fits; in Spark, compute it on `train` and
join it to `test`).

## 2. Temporal leakage

The model trains on the future relative to the rows it is evaluated on, or a feature uses values
from after the prediction time.

| Looks like | Confirm |
| --- | --- |
| `train_test_split` (shuffles by default), `KFold(shuffle=True)`, `randomSplit`, or `sample(frac=1)` on data with a date and a forecasting target | Is the task to predict a later time from earlier data? If yes, a random split leaks. |
| `rolling(..., center=True)`, `shift(-n)` used as a **feature**, `bfill`/`backfill`, `interpolate` across the split | Does the window or fill reach rows after the current timestamp? (`shift(-1)` to build the *target* is fine.) |
| Aggregates over a whole entity history (`groupby(user).transform("max")`) used to predict a point in that history | Does the aggregate include events after the prediction row? |
| A time-based split with no gap when the target looks ahead `h` steps | Do the last training rows' targets fall inside the test period? |

Fix: split on time (`TimeSeriesSplit`, or a cutoff with a gap of at least the horizon). Use
past-only windows (`shift(1).rolling(n)`). Compute "as of" aggregates.

## 3. Train/test contamination

The evaluation rows are not independent of training: the same entity is on both sides, duplicates
cross the split, or the test set steered training decisions.

| Looks like | Confirm |
| --- | --- |
| A row-level split (`train_test_split`, `randomSplit`) where an entity (user, card, patient, store) has many rows and the label is per entity | Can the same entity id appear in both splits? |
| `drop_duplicates`/`dropDuplicates` **after** the split, or no dedup on data with known duplicates | Can identical rows land on both sides? |
| A loop or search that picks hyperparameters, features, thresholds, or early stopping by test-set score | Is the reported test score the same set used to choose? |
| Oversampling (`SMOTE`, `fit_resample`) or augmentation before the split | Are synthetic test rows built from training rows, or the reverse? |

Fix: use a group split (`GroupKFold`, `GroupShuffleSplit`, or split distinct ids and join back).
Dedupe before splitting. Select on a validation split or CV, and score the test set once. Resample
inside the training fold only.

## 4. Preprocessing fit on the full dataset

A stateful transformer learns statistics from evaluation rows.

| Looks like | Confirm |
| --- | --- |
| `StandardScaler`, `MinMaxScaler`, `SimpleImputer`, `PCA`, `OneHotEncoder`, `TfidfVectorizer`, `SelectKBest` with `.fit`/`.fit_transform` called before the split | Which rows did `fit` see? |
| Spark `Imputer`, `StandardScaler`, `StringIndexer`, `Bucketizer` with quantiles, or `.fit(df)` before `randomSplit` | Same. A Spark `Pipeline.fit(train)` is fine. A stage fit separately on `df` is not. |
| `df.fillna(df.mean())`, `df[c] / df[c].max()`, or quantile clipping on the full frame | A pandas statistic is a fit too. Was it computed on all rows? |
| Feature selection by correlation with the label on all rows | Same as target leakage: the selection saw test labels. |

Stateless operations are fine before the split: `fillna(0)`, `log1p`, type casts, row filters that
don't depend on the label.

Fix: put the transformer inside a scikit-learn `Pipeline` or Spark `Pipeline` that is fit on the
training split. For CV, the pipeline goes inside the CV call.

## Not leakage (don't report)

- `shift(-1)` or similar used only to construct the target.
- `stratify=y` in a split.
- Computing the split boundary (a date quantile) on the full data.
- A fitted pipeline applied (`transform`, `predict`) to test data.
- `TargetEncoder.fit_transform` inside a scikit-learn `Pipeline` or `ColumnTransformer` (it cross-fits).
- Choosing hyperparameters with CV on the training split, then scoring the test set once.
