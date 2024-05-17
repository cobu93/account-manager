from tempfile import SpooledTemporaryFile

def download_file_from_s3(bucket_name: str, origin_file: str, destiny_file: str, s3_cli):
    s3_cli.download_file(bucket_name, origin_file, destiny_file)

def download_obj_from_s3(bucket_name: str, origin_file: str, stream: SpooledTemporaryFile, s3_cli):
    s3_cli.download_fileobj(bucket_name, origin_file, stream)

def upload_file_to_s3(bucket_name: str, origin_file: str, destiny_file: str, s3_cli):
    s3_cli.upload_file(destiny_file, bucket_name, origin_file)

def upload_obj_to_s3(bucket_name: str, destiny_file: str, stream: SpooledTemporaryFile, s3_cli):
    try:
        s3_cli.upload_fileobj(stream, bucket_name, destiny_file)
    except Exception as e:
        return dict(code=-1, message=str(e))

    return dict(code=0, message="Uploaded file")


