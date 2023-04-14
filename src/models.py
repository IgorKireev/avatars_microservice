from fastapi import UploadFile
import datetime
from pydantic import BaseModel, Field
import enum

class CreateFileUploadArgsModel(BaseModel):
    id: int = Field(example=1)
    flags: dict = Field(
     example={
        "timestamp": 123123123,
        "ip": "1.1.1.1",
        "target": "avatar"
    })

class CreateFileUploadResponseModel(BaseModel):
    url: str = Field(example='http://127.0.0.1:8000/upload/ABCDEFGHIJ')
    image_id: str = Field(example='ABCDEFGHIJ')
    key: str = Field(example='b4d508cb4d4d82d2f6b685575551d6f4')

class UploadFileResponseModel(BaseModel):
    image_id: str = Field(example='ABCDEFGHIJ')
    key: str = Field(example='b4d508cb4d4d82d2f6b685575551d6f4')
    file: UploadFile = Field(example='ABCDEFGHIJ.png')

class ChangeFileArgsModel(BaseModel):
    image_id: str = Field(example='ABCDEFGHIJ')
    secret_key: str = Field(example='123456789')

class ChangeFileResponseModel(CreateFileUploadResponseModel):
    pass

class OrderBy(enum.StrEnum):
    IMAGE_ID = 'image_id'
    KEY = 'key'
    STATUS = 'status'
    CREATED_AT = 'created_at'
    CHANGED_AT = 'changed_at'
    FLAGS = 'flags'

class Direction(enum.StrEnum):
    ASC = 'ASC'
    DESC = 'DESC'

class SearchFileArgsModel(BaseModel):
    limit: int = Field(example=10)
    offset: int = Field(example=0)
    order_by: OrderBy = Field(example=OrderBy.KEY)
    direction: Direction = Field(example=Direction.ASC)

class SearchFileEntryResponseModel(BaseModel):
    image_id: str = Field(example='ABCDEFGHIJ')
    status: bool = Field(example=False)
    created_at: datetime.timedelta
    changed_at: datetime.timedelta
    flags: dict[str, str|int|float]

class SearchFileResponseModel(BaseModel):
    count: int = Field(example=10)
    response: list[SearchFileEntryResponseModel]
    max_count: int = Field(example=100)

class DeleteFileArgsModel(BaseModel):
    image_id: str = Field(example='ABCDEFGHIJ')

class DeleteFileResponseModel(BaseModel):
    status: bool = Field(example=True)