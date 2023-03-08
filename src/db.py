import psycopg2
import config
import time

while True:
    try:
        connection = psycopg2.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.db_name
    )
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS info_avatars(
                id SERIAL PRIMARY KEY, 
                image_id VARCHAR(15) UNIQUE,
                key VARCHAR(150),
                status BOOLEAN,
                created_at TIMESTAMP DEFAULT NOW(),
                changed_at TIMESTAMP DEFAULT NOW(),
                flags JSON)
            """)
        connection.commit()
        break
    except Exception as _ex:
        print('error while working with PostgeSQL', _ex)
        time.sleep(5)

