# Контейнеры:
## База данных
### Сборка
image **[postgres:13](https://hub.docker.com/_/postgres)**
### Volumes
- `/var/lib/postgresql/data` - файлы базы данных
### Порты сервиса
- 5432 ($POSTGRES_PORT) - база данных
## Микросервис аватарок
### Сборка 
build `.`
### Volumes
- `/app/avatars` - аватарки 
### Порты сервиса
- 8000 - сервер
### Переменные окружения:
#### Настройки сервиса
- `TOKEN_CHECK: str`
#### Запуск веб сервера
- `ROOT_PATH: str`
#### Настройки базы данных
- `DB_HOST: str`
- `DB_USER: str`
- `DB_PASSWORD: str`
- `DB_NAME: str`
#### Генерация ссылки
- `BASE_URL: str` 
