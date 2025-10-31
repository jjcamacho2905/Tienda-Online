from sqlmodel import SQLModel
from typing import Optional
from pydantic import Field

# CATEGORÍAS

class CategoryBase(SQLModel):
    """
    Modelo base para las categorías.
    Contiene los campos que se usan al crear, leer o actualizar una categoría.
    """
    nombre: str = Field(min_length=3, description="Debe tener al menos 3 caracteres")
    descripcion: Optional[str] = None


class CategoryCreate(CategoryBase):
    """
    Se usa al crear una nueva categoría.
    Hereda los campos del modelo base.
    """
    pass


class CategoryRead(CategoryBase):
    """
    Se usa al devolver una categoría desde la API.
    Incluye el ID y el estado (activo o no).
    """
    id: int
    activo: bool = True

    class Config:
        from_attributes = True  # Permite convertir objetos SQLModel a esquemas Pydantic


class CategoryUpdate(SQLModel):
    """
    Se usa para actualizar una categoría existente.
    Los campos son opcionales para poder cambiar solo lo necesario.
    """
    nombre: Optional[str] = Field(default=None, min_length=3)
    descripcion: Optional[str] = None


# PRODUCTOS

class ProductBase(SQLModel):
    """
    Modelo base para los productos.
    Define los campos principales que se usan en varios esquemas.
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
    Se usa al crear un producto nuevo.
    Hereda los campos del modelo base.
    """
    id: int

    class Config:
        from_attributes = True  # Convierte automáticamente objetos SQLModel a Pydantic


class ProductUpdate(SQLModel):
    """
    Se usa para actualizar un producto existente.
    Todos los campos son opcionales, por si se quiere modificar solo algunos.
    """
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    cantidad: Optional[int] = None
    categoria_id: Optional[int] = None
    activo: Optional[bool] = None
