import logging
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min, max, lit

# Configuracao de logs de aplicacao
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger("datalake_enem_small_upsert")
logger.setLevel(logging.DEBUG)

# Definicao da Spark Session
spark = (
    SparkSession.builder.appName("DeltaExercise")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    .config("spark.databricks.delta.retentionDurationCheck.enabled", "false")
    .getOrCreate()
)


logger.info("Importing delta.tables...")
from delta.tables import *


logger.info("Produzindo novos dados...")
enemnovo = spark.read.format("delta").load(
    "s3://datalake-kraisfeld-igti-edc-tf/staging-zone/enem"
)

# Define algumas inscricoes (chaves) que serao alteradas
inscricoes = [
    200006271946,
    200001195856,
    200001943954,
    200001908998,
    200001634757,
    200003132410,
    200001379770,
    200001334237,
    200006762554,
    200005146210,
    200004902048,
    200006138472,
    200005613689,
    200004833505,
    200004570764,
    200001071590,
    200001934470,
    200006066678,
    200003343448,
]


logger.info("Reduz a 50 casos e faz updates internos no municipio de residencia")
enemnovo = enemnovo.where(enemnovo.NU_INSCRICAO.isin(inscricoes))
enemnovo = enemnovo.withColumn(
    "NO_MUNICIPIO_RESIDENCIA", lit("NOVA CIDADE")
).withColumn("CO_MUNICIPIO_RESIDENCIA", lit(10000000))


logger.info("Pega os dados do Enem velhos na tabela Delta...")
enemvelho = DeltaTable.forPath(
    spark, "s3://datalake-kraisfeld-igti-edc-tf/staging-zone/enem"
)


logger.info("Realiza o UPSERT...")
(
    enemvelho.alias("old")
    .merge(enemnovo.alias("new"), "old.NU_INSCRICAO = new.NU_INSCRICAO")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

logger.info("Atualizacao completa! \n\n")

logger.info("Gera manifesto symlink...")
enemvelho.generate("symlink_format_manifest")

logger.info("Manifesto gerado.")
