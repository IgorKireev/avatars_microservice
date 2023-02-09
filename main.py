from fastapi import FastAPI, UploadFile, Path, File, Query
from pydantic import BaseModel, Field
import random
import string

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
    key: str = Field(example='0x7487b4a3')

app = FastAPI()

@app.post(
    '/create',
    summary = 'Создание ссылки для загрузки файлов',
    responses= {
        200: {
            'model': CreateFileUploadResponseModel,
            'description': 'Ссылка для загрузки файла успешно создана'
        }
    }
)
def create(form: CreateFileUploadArgsModel):
    array = [random.choice(string.ascii_uppercase) for i in range(10)]
    image_id = ''.join(array)
    url = f'/upload/{image_id}'
    key = hex(random.randint(1, 100000000))
    return {'url': url, 'image_id': image_id, 'key':key}

@app.post(
    '/upload/{image_id}',
    summary='Загрузка файла'
)
async def get_upload(
        file: UploadFile = File(description='Image uploaded by the client', example='Makima.jpg'),
        image_id: str = Path(description='The ID of the image to get', example='ABCDEFGHIJ'),
        key: str = Query(description='a unique key is generated for each image', example='0x7487b4a3')
):
     with open(f'avatars/{image_id}.jpg', 'wb') as save_file:
        save_file.write(await file.read())
     return {'image_id':image_id, 'key':key, 'file':file}


