import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max, min

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

print("Spark configuration...")
# Cria objeto da Spark Session
spark = (
    SparkSession.builder.appName("DeltaExercise")
    .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY_ID)
    .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0,org.apache.hadoop:hadoop-aws:3.1.2,io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.hadoop.fs.s3a.fast.upload", True)
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    .getOrCreate()
)
spark._jsc.hadoopConfiguration().set(
    "fs.s3a.aws.credentials.provider",
    "com.amazonaws.auth.InstanceProfileCredentialsProvider,com.amazonaws.auth.DefaultAWSCredentialsProviderChain",
)
# Importa o modulo das tabelas delta
from delta.tables import *

print("Reading data...")
# Leitura de dados
enem = (
    spark.read.format("csv")
    .option("inferSchema", True)
    .option("header", True)
    .option("delimiter", ",")
    .load("s3a://datalake-kraisfeld-igti-edc/raw-data/enem")
)
[print(col) for col in enem.columns]
# Escreve a tabela em staging em formato delta
print("Writing delta table...")
(
    enem.write.mode("overwrite")
    .format("delta")
    .partitionBy("TP_ANO_CONCLUIU")
    .save("s3a://datalake-kraisfeld-igti-edc-tf/staging-zone/enem")
)
