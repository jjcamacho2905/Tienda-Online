from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tienda.db")

motor = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(motor)

def get_session():
    with Session(motor) as session:
        yield session


