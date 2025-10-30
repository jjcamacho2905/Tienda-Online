from typing import Optional
from sqlmodel import SQLModel


# ==========================
# CATEGORÍAS
# ==========================
class CategoryBase(SQLModel):
    nombre: str
    descripcion: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class CategoryUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


# ==========================
# PRODUCTOS
# ==========================
class ProductBase(SQLModel):
    nombre: str
    precio: float
    cantidad: int
    categoria_id: int
    activo: Optional[bool] = True


class ProductCreate(SQLModel):  # 👈 ya no hereda de ProductBase
    nombre: str
    precio: float
    cantidad: int
    categoria_id: int


class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True


class ProductUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    cantidad: Optional[int] = None
    categoria_id: Optional[int] = None
    activo: Optional[bool] = None