import config
import os
import boto3
from pathlib import Path
from datetime import datetime
from kaggle.api.kaggle_api_extended import KaggleApi
from botocore.exceptions import ClientError


data_folder = Path(__file__).resolve().parent / 'data'
data_folder.mkdir(parents=True, exist_ok=True)
log_file = data_folder / 'log.txt'

s3 = boto3.client('s3', **config.MINIO_CONFIG)

try:
    s3.create_bucket(Bucket=config.MINIO_BUCKET_NAME)
except:
    pass

print("===Kiểm tra dữ liệu trên Kaggle===")
dataset_name = 'olistbr/brazilian-ecommerce'
os.environ['KAGGLE_API_TOKEN'] = config.KAGGLE_API_TOKEN
api = KaggleApi()
api.authenticate()
remote_dataset = next((ds for ds in api.dataset_list(search=dataset_name) if ds.ref == dataset_name), None)
should_download = False
remote_last_updated = remote_dataset.last_updated.date()
local_last_updated = None

if log_file.exists():
    try:
        content = log_file.read_text().strip()
        local_last_updated = datetime.strptime(content, "%Y-%m-%d").date()
    except:
        pass

if local_last_updated is None or remote_last_updated > local_last_updated:
    print("Có cập nhật, chuẩn bị download từ Kaggle")
    should_download = True

if should_download:
    for file in data_folder.glob('*.csv'):
        file.unlink()
    api.dataset_download_files(dataset_name, path=data_folder, unzip=True)
    log_file.write_text(str(remote_last_updated))
    print("Đã download xong")

print("===Kiểm tra dữ liệu trên MinIO===")
for file in data_folder.glob('*.csv'):
    local_size = file.stat().st_size
    should_upload = should_download
    
    if not should_upload:
        try :
            remote_size = s3.head_object(Bucket=config.MINIO_BUCKET_NAME, Key=file.name)['ContentLength']

            if remote_size != local_size:
                print(f"Có cập nhật, chuẩn bị upload file {file.name} lên MinIO")
                should_upload = True

        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                should_upload = True
            else:
                print(f"Lỗi khi kiểm tra file {file.name}: {e}")

    if should_upload:
        print(f"Upload file {file.name} xong")
        s3.upload_file(str(file), config.MINIO_BUCKET_NAME, file.name)
