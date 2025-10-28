from sqlmodel import SQLModel, create_engine, Session

# Conexión a la base de datos SQLite
DATABASE_URL = "sqlite:///tienda.db"
engine = create_engine(DATABASE_URL, echo=True)

# Crear las tablas
def init_db():
    SQLModel.metadata.create_all(engine)

# Sesión de base de datos
def get_session():
    with Session(engine) as session:
        yield session
