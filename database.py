from sqlmodel import create_engine

# Conexión a la base de datos SQLite
motor = create_engine("sqlite:///tienda.db", echo=True)
