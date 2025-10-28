from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


# MODELO DE CATEGORÍA
class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None

    # Relación: una categoría puede tener varios productos
    productos: List["Producto"] = Relationship(back_populates="categoria")


# MODELO DE PRODUCTO
class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    precio: float
    stock: int
    activo: bool = True
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")

    # Relación inversa hacia la categoría
    categoria: Optional[Categoria] = Relationship(back_populates="productos")
