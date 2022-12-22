from fastapi import FastAPI
from pydantic import BaseModel
from random import choice
from string import ascii_uppercase
import os

class CreateFileUploadArgsModel(BaseModel):
    id: int
    flags: dict

class CreateFileUploadResponseModel(BaseModel):
    url: str
    image_id: str

app = FastAPI()

@app.post(
    '/create',
    summary = 'Создание ссылки для загрузки файлов',
    responses= {
        200: {
            'model': CreateFileUploadResponseModel,
            'description': 'Ссылка для загрузки файла успешно создана',
            'example': CreateFileUploadResponseModel(
                url = 'http://127.0.0.1:8000/upload/EIFWEFW',
                image_id = 'EIFWEFW'
            )
        }
    }
)



def create(form: CreateFileUploadArgsModel):
    array = [choice(ascii_uppercase) for i in range(30)]
    image_id = ''.join(array)
    return {'url': url, 'image_id': image_id}