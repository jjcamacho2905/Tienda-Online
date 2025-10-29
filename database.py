from sqlmodel import SQLModel, create_engine, Session

# Nombre del archivo de base de datos SQLite
DATABASE_URL = "sqlite:///./tienda.db"

# Motor de conexión
motor = create_engine(DATABASE_URL, echo=True)

# Inicializa la base de datos (crea tablas si no existen)
def init_db():
    SQLModel.metadata.create_all(motor)

# Devuelve una sesión de base de datos
def get_session():
    with Session(motor) as session:
        yield session


