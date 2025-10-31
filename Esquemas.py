from sqlmodel import SQLModel
from typing import Optional
from pydantic import Field

# CATEGORÍAS

class CategoryBase(SQLModel):
    """
    Esquema base para las categorías.
    Contiene los campos comunes utilizados en creación, lectura y actualización.
    """
    nombre: str = Field(min_length=3, description="Debe tener al menos 3 caracteres")
    descripcion: Optional[str] = None


class CategoryCreate(CategoryBase):
    """
    Esquema utilizado para crear una nueva categoría.
    Hereda todos los campos del esquema base (CategoryBase).
    """
    pass


class CategoryRead(CategoryBase):
    """
    Esquema utilizado para la lectura (salida) de categorías.
    Incluye el identificador y el estado activo de la categoría.
    """
    id: int
    activo: bool = True

    class Config:
        from_attributes = True  # Permite convertir objetos SQLModel a esquemas Pydantic


class CategoryUpdate(SQLModel):
    """
    Esquema utilizado para actualizar una categoría existente.
    Todos los campos son opcionales, permitiendo actualizaciones parciales.
    """
    nombre: Optional[str] = Field(default=None, min_length=3)
    descripcion: Optional[str] = None


# PRODUCTOS

class ProductBase(SQLModel):
    """
    Esquema base para los productos.
    Define los campos principales que se reutilizan en creación, lectura y actualización.
    """
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    cantidad: int
    categoria_id: int
    activo: Optional[bool] = True


class ProductCreate(ProductBase):
    """
    Esquema utilizado para crear un nuevo producto.
    Hereda todos los campos del esquema base (ProductBase).
    """
    pass


class ProductRead(ProductBase):
    """
    Esquema utilizado para la lectura (salida) de productos.
    Incluye el identificador del producto.
    """
    id: int

    class Config:
        from_attributes = True  # Convierte automáticamente objetos SQLModel a Pydantic


class ProductUpdate(SQLModel):
    """
    Esquema utilizado para actualizar productos existentes.
    Todos los campos son opcionales, permitiendo actualizaciones parciales (PUT/PATCH).
    """
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    cantidad: Optional[int] = None
    categoria_id: Optional[int] = None
    activo: Optional[bool] = None
