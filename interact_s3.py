import boto3
import pandas as pd

# Criar um cliente para interagir com o AWS S3
s3_client = boto3.client("s3")

s3_client.download_file(
    "datalake-kraisfeld-igti-edc",
    "data/razer-vortex-1920x1080.jpg",
    "data/razer-vortex-1920x1080.jpg",
)

s3_client.upload_file(
    "data/razer-vortex-1920x1080.jpg",
    "datalake-kraisfeld-igti-edc",
    "data/razer-vortex-1920x1080.jpg",
)
