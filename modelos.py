from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: Optional[str] = None

    # Relación con productos
    productos: List["Producto"] = Relationship(
        back_populates="categoria",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    precio: float
    cantidad: int
    activo: bool = Field(default=True)  # 👈 valor por defecto TRUE
    categoria_id: int = Field(foreign_key="categoria.id")

    # Relación inversa
    categoria: Optional[Categoria] = Relationship(back_populates="productos")


