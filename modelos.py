from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = Field(default=True)

    productos: List["Producto"] = Relationship(
        back_populates="categoria",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )



class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    cantidad: int
    activo: bool = Field(default=True)
    categoria_id: int = Field(foreign_key="categoria.id")

    categoria: Optional[Categoria] = Relationship(back_populates="productos")


