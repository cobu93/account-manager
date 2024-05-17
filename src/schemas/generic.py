from pydantic import BaseModel

class GenericResponse(BaseModel):
    message: str
    code: int