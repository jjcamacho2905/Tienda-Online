# rutas.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional

from database import get_session
from modelos import Categoria, Producto
from esquemas import (
    CategoriaCrear, CategoriaLeer, CategoriaActualizar,
    ProductoCrear, ProductoLeer, ProductoActualizar
)

router = APIRouter()


# ----------------------
# CATEGORÍAS
# ----------------------

@router.post("/categorias", response_model=CategoriaLeer, status_code=status.HTTP_201_CREATED)
def crear_categoria(data: CategoriaCrear, session: Session = Depends(get_session)):
    # Regla: nombre de categoría único => 409 Conflict
    existente = session.exec(select(Categoria).where(Categoria.nombre == data.nombre)).first()
    if existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nombre de la categoría ya existe.")
    categoria = Categoria.from_orm(data)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


@router.get("/categorias", response_model=List[CategoriaLeer])
def listar_categorias_activas(session: Session = Depends(get_session)):
    # Listar solo categorías activas
    return session.exec(select(Categoria).where(Categoria.activa == True)).all()


@router.get("/categorias/{categoria_id}", response_model=CategoriaLeer)
def obtener_categoria_con_productos(categoria_id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada.")
    # Si quieres devolver productos incluidos, SQLModel los mostrará si la relación está definida.
    return categoria


@router.put("/categorias/{categoria_id}", response_model=CategoriaLeer)
def actualizar_categoria(categoria_id: int, data: CategoriaActualizar, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada.")
    # Si cambia el nombre, asegurar unicidad
    if data.nombre and data.nombre != categoria.nombre:
        otra = session.exec(select(Categoria).where(Categoria.nombre == data.nombre)).first()
        if otra:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Otro registro ya usa este nombre de categoría.")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(categoria, k, v)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


@router.delete("/categorias/{categoria_id}")
def desactivar_categoria(categoria_id: int, session: Session = Depends(get_session)):
    """
    Desactivación (soft-delete): marca la categoría como inactiva
    y desactiva (soft) todos los productos asociados (regla de cascada soft).
    """
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada.")
    categoria.activa = False
    session.add(categoria)
    productos = session.exec(select(Producto).where(Producto.categoria_id == categoria_id)).all()
    for p in productos:
        p.activo = False
        session.add(p)
    session.commit()
    return {"mensaje": "Categoría desactivada y productos asociados desactivados."}


# ----------------------
# PRODUCTOS
# ----------------------

@router.post("/productos", response_model=ProductoLeer, status_code=status.HTTP_201_CREATED)
def crear_producto(data: ProductoCrear, session: Session = Depends(get_session)):
    # Regla: producto debe pertenecer a una categoría existente y activa
    categoria = session.get(Categoria, data.categoria_id)
    if not categoria or not categoria.activa:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoría inválida o inactiva.")
    # stock y precio validados por esquemas (>=0)
    producto = Producto.from_orm(data)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.get("/productos", response_model=List[ProductoLeer])
def listar_productos(
    min_stock: Optional[int] = Query(None, ge=0),
    max_precio: Optional[float] = Query(None, ge=0),
    categoria_id: Optional[int] = Query(None),
    activo: Optional[bool] = Query(True),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session)
):
    """
    Listar productos con filtros:
    - min_stock: filtra por stock >= min_stock
    - max_precio: filtra por precio <= max_precio
    - categoria_id: filtra por categoría
    - activo: True/False (por defecto True, solo productos activos)
    """
    stmt = select(Producto)
    if min_stock is not None:
        stmt = stmt.where(Producto.stock >= min_stock)
    if max_precio is not None:
        stmt = stmt.where(Producto.precio <= max_precio)
    if categoria_id is not None:
        stmt = stmt.where(Producto.categoria_id == categoria_id)
    if activo is not None:
        stmt = stmt.where(Producto.activo == activo)
    # paginación simple
    resultados = session.exec(stmt.offset(offset).limit(limit)).all()
    return resultados


@router.get("/productos/{producto_id}", response_model=ProductoLeer)
def obtener_producto_con_categoria(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    return producto


@router.put("/productos/{producto_id}", response_model=ProductoLeer)
def actualizar_producto(producto_id: int, data: ProductoActualizar, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    # Si cambian categoría, validar que exista y esté activa
    if data.categoria_id is not None and data.categoria_id != producto.categoria_id:
        categoria = session.get(Categoria, data.categoria_id)
        if not categoria or not categoria.activa:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nueva categoría inválida o inactiva.")
    # Si actualizan stock o precio, los esquemas ya validan >= 0
    for k, v in data.dict(exclude_unset=True).items():
        setattr(producto, k, v)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.delete("/productos/{producto_id}")
def desactivar_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    producto.activo = False
    session.add(producto)
    session.commit()
    return {"mensaje": "Producto desactivado correctamente."}


@router.post("/productos/{producto_id}/restock", response_model=ProductoLeer)
def reponer_stock(producto_id: int, cantidad: int = Query(..., gt=0), session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    producto.stock += cantidad
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.post("/productos/{producto_id}/comprar", response_model=ProductoLeer)
def comprar_producto(producto_id: int, cantidad: int = Query(..., gt=0), session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado.")
    if not producto.activo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Producto inactivo.")
    if producto.stock < cantidad:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock insuficiente.")
    producto.stock -= cantidad
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto
