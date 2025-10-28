from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# ======================
# MODELOS DE CATEGORÍAS
# ======================
class CategoryBase(SQLModel):
    nombre: str
    descripcion: Optional[str] = None


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    productos: list["Product"] = Relationship(back_populates="categoria")


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int


class CategoryUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


# ===================
# MODELOS DE PRODUCTOS
# ===================
class ProductBase(SQLModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    cantidad: int = 0
    categoria_id: Optional[int] = Field(default=None, foreign_key="category.id")


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    categoria: Optional[Category] = Relationship(back_populates="productos")


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int


class ProductUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    cantidad: Optional[int] = None
    categoria_id: Optional[int] = None
