from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# MODELO DE CATEGORÍA
class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    activa: bool = True

    productos: List["Producto"] = Relationship(back_populates="categoria")


# MODELO DE PRODUCTO
class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    precio: float
    stock: int
    activo: bool = True
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")

    categoria: Optional[Categoria] = Relationship(back_populates="productos")