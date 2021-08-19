import os
from dotenv import load_dotenv
import jwt

from minio import Minio

from src import app

load_dotenv()

ENDPOINT_URL = os.environ['MLFLOW_S3_ENDPOINT_URL']
ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

os.environ['AUTH_TOKEN'] = jwt.encode(
    {"token": str(os.environ.get("SECRET_KEY"))}, "secret", algorithm="HS256"
)

if os.environ['FLASK_ENV'] == 'development':
    minio_client = Minio(ENDPOINT_URL.split('//')[1],
                        access_key=ACCESS_KEY,
                        secret_key=SECRET_KEY,
                        secure=False)

    buckets = minio_client.list_buckets()
    if 'mlflow' not in [bucket.name for bucket in buckets]:
        minio_client.make_bucket('mlflow')
        
        with open('policy.json') as f:
            policy = f.read()
        minio_client.set_bucket_policy('mlflow', policy)

app.run(debug=True, host='0.0.0.0')
