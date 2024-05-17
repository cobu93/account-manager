from ..config import S3_ACCESS_KEY, S3_SECRET_KEY, BOTO3_ENDPOINT
from boto3.session import Session


def get_s3_client():
    session = Session(
                aws_access_key_id=S3_ACCESS_KEY,
                aws_secret_access_key=S3_SECRET_KEY
            )
    
    s3 = session.client("s3", endpoint_url=BOTO3_ENDPOINT)
        
    try:
        yield s3
    finally:
        s3.close()
        pass

