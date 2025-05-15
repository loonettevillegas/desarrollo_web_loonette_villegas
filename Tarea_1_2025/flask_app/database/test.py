from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"  # Usa el usuario que quieres probar
DB_PASSWORD = "programacionweb" # Usa la contraseña del usuario
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URL)
    engine.connect()  # Intenta establecer la conexión
    print("¡Conexión a la base de datos exitosa!")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
finally:
    if 'engine' in locals() and engine:
        engine.dispose() # Cierra las conexiones