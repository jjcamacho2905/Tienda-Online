from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from database import get_session
from modelos import Categoria, Producto
from Esquemas import CategoryCreate, CategoryRead, CategoryUpdate, ProductCreate, ProductRead, ProductUpdate
from typing import Optional, List

router = APIRouter()

# CRUD DE CATEGORÍAS


@router.get("/categorias", response_model=List[CategoryRead], status_code=status.HTTP_200_OK)
def listar_categorias(session: Session = Depends(get_session)):
    """
    Obtiene todas las categorías activas.
    """
    categorias = session.exec(select(Categoria).where(Categoria.activo == True)).all()
    if not categorias:
        raise HTTPException(status_code=404, detail="No hay categorías registradas.")
    return categorias


@router.get("/categorias/{id}", response_model=CategoryRead, status_code=status.HTTP_200_OK)
def obtener_categoria(id: int, session: Session = Depends(get_session)):
    """
    Obtiene una categoría por su ID.
    """
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    return categoria


@router.post("/categorias", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def crear_categoria(data: CategoryCreate, session: Session = Depends(get_session)):
    """
    Crea una nueva categoría.
    """
    existente = session.exec(select(Categoria).where(Categoria.nombre == data.nombre)).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe una categoría con ese nombre.")

    nueva_categoria = Categoria.from_orm(data)
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    return nueva_categoria


@router.put("/categorias/{id}", response_model=CategoryRead, status_code=status.HTTP_200_OK)
def actualizar_categoria(id: int, data: CategoryUpdate, session: Session = Depends(get_session)):
    """
    Actualiza una categoría existente.
    """
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(categoria, key, value)

    session.commit()
    session.refresh(categoria)
    return categoria


@router.delete("/categorias/{id}", status_code=status.HTTP_200_OK)
def eliminar_categoria(id: int, session: Session = Depends(get_session)):
    """
    Desactiva una categoría (eliminación lógica).
    """
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")

    categoria.activo = False
    session.commit()
    return {"message": "Categoría desactivada correctamente."}


@router.get("/categorias/{id_categoria}/productos", response_model=CategoryRead, status_code=status.HTTP_200_OK)
def categoria_con_productos(id_categoria: int, session: Session = Depends(get_session)):
    """
    Obtiene una categoría junto con sus productos.
    """
    categoria = session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    return categoria


# CRUD DE PRODUCTOS


@router.post("/productos", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductCreate, session: Session = Depends(get_session)):
    """
    Crea un nuevo producto asociado a una categoría existente.
    """
    categoria = session.get(Categoria, producto.categoria_id)
    if not categoria:
        raise HTTPException(status_code=400, detail="La categoría no existe.")

    existente = session.exec(select(Producto).where(Producto.nombre == producto.nombre)).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe un producto con ese nombre.")

    producto_db = Producto.from_orm(producto)
    session.add(producto_db)
    session.commit()
    session.refresh(producto_db)
    return producto_db


@router.get("/productos", response_model=List[ProductRead], status_code=status.HTTP_200_OK)
def listar_productos(
        stock_min: Optional[int] = Query(None),
        precio_max: Optional[float] = Query(None),
        categoria_id: Optional[int] = Query(None),
        session: Session = Depends(get_session)
):
    """
    Lista productos con filtros opcionales: stock mínimo, precio máximo y categoría.
    """
    consulta = select(Producto).where(Producto.activo == True)

    if stock_min is not None:
        consulta = consulta.where(Producto.cantidad >= stock_min)
    if precio_max is not None:
        consulta = consulta.where(Producto.precio <= precio_max)
    if categoria_id is not None:
        consulta = consulta.where(Producto.categoria_id == categoria_id)

    productos = session.exec(consulta).all()
    if not productos:
        raise HTTPException(status_code=404, detail="No se encontraron productos con los filtros aplicados.")
    return productos


@router.get("/productos/{producto_id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    """
    Obtiene un producto por su ID.
    """
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return producto


@router.put("/productos/{producto_id}", response_model=ProductRead, status_code=status.HTTP_200_OK)
def actualizar_producto(producto_id: int, data: ProductUpdate, session: Session = Depends(get_session)):
    """
    Actualiza los datos de un producto existente.
    """
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(producto, key, value)

    session.commit()
    session.refresh(producto)
    return producto


@router.delete("/productos/{producto_id}", status_code=status.HTTP_200_OK)
def eliminar_producto(producto_id: int, session: Session = Depends(get_session)):
    """
    Desactiva un producto (eliminación lógica).
    """
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")

    producto.activo = False
    session.commit()
    return {"message": "Producto desactivado correctamente."}


@router.put("/productos/{producto_id}/comprar", response_model=ProductRead, status_code=status.HTTP_200_OK)
def comprar_producto(producto_id: int, cantidad: int, session: Session = Depends(get_session)):
    """
    Realiza la compra de un producto, restando del stock la cantidad comprada.
    """
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    if cantidad <= 0:
        raise HTTPException(status_code=400, detail="Cantidad inválida.")
    if producto.cantidad < cantidad:
        raise HTTPException(status_code=400, detail="No hay suficiente stock disponible.")

    producto.cantidad -= cantidad
    session.commit()
    session.refresh(producto)
    return producto
