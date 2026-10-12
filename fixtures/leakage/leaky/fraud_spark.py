"""Score card transactions for fraud with a Spark ML pipeline."""

from pyspark.ml import Pipeline
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import Imputer, VectorAssembler
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("fraud").getOrCreate()

# One row per transaction; many transactions per card. Label: the card was confirmed compromised.
tx = spark.read.parquet("data/transactions.parquet")

numeric = ["amount", "merchant_risk", "hours_since_prev_tx"]
imputer = Imputer(inputCols=numeric, outputCols=[f"{c}_imp" for c in numeric]).fit(tx)
tx = imputer.transform(tx)

train, test = tx.randomSplit([0.8, 0.2], seed=7)

assembler = VectorAssembler(inputCols=[f"{c}_imp" for c in numeric], outputCol="features")
gbt = GBTClassifier(labelCol="card_compromised", featuresCol="features")
model = Pipeline(stages=[assembler, gbt]).fit(train)

auc = BinaryClassificationEvaluator(labelCol="card_compromised").evaluate(model.transform(test))
print(f"test AUC {auc:.3f}")
