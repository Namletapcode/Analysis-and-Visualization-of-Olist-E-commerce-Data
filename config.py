import os
from dotenv import load_dotenv

load_dotenv()

KAGGLE_API_TOKEN = os.getenv('KAGGLE_API_TOKEN')

MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = 'olist-data'
MINIO_CONFIG = {
    'endpoint_url': MINIO_ENDPOINT,
    'aws_access_key_id': MINIO_ACCESS_KEY,
    'aws_secret_access_key': MINIO_SECRET_KEY
}

MYSQL_URL = os.getenv('MYSQL_URL')
MYSQL_PROPERTIES = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'driver': os.getenv('MYSQL_DRIVER')
}
