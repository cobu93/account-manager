from pydantic import BaseModel

class FileDescription(BaseModel):
    path: str = "."
    file_name: str = "transactions.csv"

class S3FileDescription(FileDescription):
    bucket: str = "account-manager"