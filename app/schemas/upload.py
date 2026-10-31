from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    file_name: str
    pages: int
    chunks: int
