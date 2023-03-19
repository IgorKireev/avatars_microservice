import os

host = os.getenv('DB_HOST', 'db')
user = os.getenv('DB_USER', 'postgres')
password = os.getenv('DB_PASSWORD', 'postgres')
db_name = os.getenv('DB_NAME', 'postgres')

