from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv


# CONFIGURACIÓN DE CONEXIÓN A LA BASE DE DATOS


# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene la URL de la base de datos desde las variables de entorno (.env)
# Si no se encuentra, utiliza por defecto una base SQLite local.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tienda.db")

# Crea el motor (engine) de conexión a la base de datos
# 'echo=True' permite mostrar las consultas SQL ejecutadas en consola (modo depuración)
motor = create_engine(DATABASE_URL, echo=True)


def init_db():
    """
    Crea las tablas definidas en los modelos.
    """
    SQLModel.metadata.create_all(motor)


def get_session():
    """
    Devuelve una sesión activa con la base de datos.
    Se usa como dependencia en los endpoints.
    """
    with Session(motor) as session:
        yield session


