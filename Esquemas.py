from typing import Optional, List
from sqlmodel import SQLModel

# CATEGORÍAS
class CategoryBase(SQLModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    activo: bool = True


    class Config:
        from_attributes = True

class CategoryUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None




# PRODUCTOS

class ProductBase(SQLModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    cantidad: int
    categoria_id: int
    activo: Optional[bool] = True


class ProductCreate(ProductBase):
    pass


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