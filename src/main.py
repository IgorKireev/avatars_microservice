from typing import Annotated
import fastapi
from fastapi import *
import random
import string
from db import connection
from json import dumps
from secrets import token_bytes
from models import *
import config
import os

app = FastAPI()

async def get_token_header(x_token: str = Header(description='key for private url', example='2e3852bfdd5ac217592feb198051f8a8')):
    if x_token != config.token:
        raise HTTPException(status_code=400, detail="X-Token header invalid")

public = fastapi.APIRouter(prefix="/public", tags=['public'])
private = fastapi.APIRouter(prefix="/private", tags=['private'], dependencies=[Depends(get_token_header)])

@private.post(
    '/create',
    summary = 'Создание ссылки для загрузки файлов',
    responses= {
        200: {
            'model': CreateFileUploadResponseModel,
            'description': 'Ссылка для загрузки файла успешно создана'
        }
    }
)
def create_file(form: CreateFileUploadArgsModel):
    array = [random.choice(string.ascii_uppercase) for i in range(10)]
    key = token_bytes(16).hex()
    while True:
        try:
            image_id = ''.join(array)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO info_avatars(image_id, key, status, flags)
                    VALUES(%s, %s, FALSE, %s)
                        """, (image_id, key, dumps(form.flags)))
                connection.commit()
                url = f'{config.base_url}/upload/{image_id}'
            break
        except :
            print('Error')
    return CreateFileUploadResponseModel(url=url, image_id=image_id, key=key)

@public.post(
    '/upload/{image_id}',
    summary='Загрузка файла',
    responses= {
        200: {
            'model': UploadFileResponseModel,
            'description': 'Файл успешно загружен'
        }
    }
)
async def upload_media(
    file: UploadFile = File(description='Image uploaded by the client', example='Makima.jpg'),
    image_id: str = Path(description='The ID of the image to get', example='ABCDEFGHIJ'),
    key: str = Query(description='a unique key is generated for each image', example='b4d508cb4d4d82d2f6b685575551d6f4')
) -> UploadFileResponseModel:
    with connection.cursor() as cursor:
        cursor.execute("""
             SELECT status
             FROM info_avatars
             WHERE image_id=%s AND info_avatars.key=%s
             """, (image_id, key))
        result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail='not found')
    if result[0]:
        raise HTTPException(status_code=404, detail='stop upload')
    with open(f'avatars/{image_id}.jpg', 'wb') as save_file:
        save_file.write(await file.read())
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE info_avatars
            SET status=TRUE 
            WHERE image_id=%s
        """, (image_id,))
    connection.commit()
    return  UploadFileResponseModel(image_id=image_id, key=key, file=file)

@private.post(
    '/change',
    summary='Изменение файла',
    responses= {
        200: {
            'description': 'Файл успешно изменён'
        }
    }
)
def change_file(form: ChangeFileArgsModel) -> ChangeFileResponseModel:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 1
            FROM info_avatars
            WHERE image_id=%s       
        """, (form.image_id,))
        result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail='not exists')
    key = token_bytes(16).hex()
    with connection.cursor() as cursor:
        cursor.execute("""
               UPDATE info_avatars
               SET status=FALSE, key=%s, changed_at=NOW()
               WHERE image_id=%s
           """, (key, form.image_id))
    connection.commit()
    url = f'/upload/{form.image_id}'
    return ChangeFileResponseModel(url=url, image_id=form.image_id, key=key)

@private.post(
    '/search',
    summary='Получение информации из бд по аватаркам',
    responses= {
        200: {
            'model': SearchFileResponseModel,
            'description': 'Информация успешно получена'
        }
    }
)
def search_files(form: SearchFileArgsModel):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT *
            FROM info_avatars
            ORDER BY {form.order_by} {form.direction}
            LIMIT %s OFFSET {form.offset}
        """, (form.limit, ))
        response = [SearchFileEntryResponseModel(
                image_id=i[1],
                status=i[3],
                created_at=i[4].timestamp(),
                changed_at=i[5].timestamp(),
                flags=i[6]
            ) for i in cursor.fetchall()
        ]
        count = len(response)
        cursor.execute("""
            SELECT COUNT(1)
            FROM info_avatars
        """)
        max_count = cursor.fetchone()[0]
    return SearchFileResponseModel(count=count, response=response, max_count=max_count)


@private.post(
    '/delete',
summary='Удаление файла',
    responses= {
        200: {
            'model': DeleteFileResponseModel,
            'description': 'Файл успешно удалён'
        }
    }
)
def delete_files(form: DeleteFileArgsModel):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 1
            FROM info_avatars
            WHERE image_id=%s       
        """, (form.image_id,))
        result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail='not exists image_id')
    with connection.cursor() as cursor:
        cursor.execute("""
               DELETE FROM info_avatars
               WHERE image_id=%s
           """, (form.image_id,))
    connection.commit()
    try:
        os.remove(f'avatars/{form.image_id}.jpg')
    except:
        raise HTTPException(status_code=404, detail='not found file for delete')
    return DeleteFileResponseModel(status=True)

app.include_router(public)
app.include_router(private)