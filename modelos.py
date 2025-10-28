from sqlmodel import SQLModel, Field
from typing import Optional

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None


# MODELO DE PRODUCTO
class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    precio: float
    stock: int
    activo: bool = True
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")

    categoria: Optional[Categoria] = Relationship(back_populates="productos")