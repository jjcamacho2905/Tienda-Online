from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import get_session
from modelos import Categoria, Producto
from Esquemas import CategoryCreate, CategoryRead, CategoryUpdate, ProductCreate, ProductRead, ProductUpdate
from typing import Optional, List

router = APIRouter()

# ======================
# CRUD DE CATEGORÍAS
# ======================

@router.get("/categorias", response_model=List[CategoryRead])
def listar_categorias(session: Session = Depends(get_session)):
    return session.exec(select(Categoria).where(Categoria.activo == True)).all()

@router.get("/categorias/{id}", response_model=CategoryRead)
def obtener_categoria(id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.put("/categorias/{id}", response_model=CategoryRead)
def actualizar_categoria(id: int, data: CategoryUpdate, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(categoria, key, value)
    session.commit()
    session.refresh(categoria)
    return categoria

@router.delete("/categorias/{id}")
def eliminar_categoria(id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    categoria.activo = False
    session.commit()
    return {"message": "Categoría desactivada correctamente"}

@router.get("/categorias/{id_categoria}/productos", response_model=CategoryRead)
def categoria_con_productos(id_categoria: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


# ======================
# CRUD DE PRODUCTOS
# ======================

@router.post("/productos", response_model=ProductRead)
def crear_producto(producto: ProductCreate, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, producto.categoria_id)
    if not categoria:
        raise HTTPException(status_code=400, detail="La categoría no existe.")

    producto_db = Producto.from_orm(producto)
    session.add(producto_db)
    session.commit()
    session.refresh(producto_db)
    return producto_db

@router.get("/productos", response_model=List[ProductRead])
def listar_productos(
    stock_min: Optional[int] = Query(None),
    precio_max: Optional[float] = Query(None),
    categoria_id: Optional[int] = Query(None),
    session: Session = Depends(get_session)
):
    consulta = select(Producto)
    if stock_min is not None:
        consulta = consulta.where(Producto.cantidad >= stock_min)
    if precio_max is not None:
        consulta = consulta.where(Producto.precio <= precio_max)
    if categoria_id is not None:
        consulta = consulta.where(Producto.categoria_id == categoria_id)
    return session.exec(consulta).all()

@router.get("/productos/{producto_id}", response_model=ProductRead)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/productos/{producto_id}", response_model=ProductRead)
def actualizar_producto(producto_id: int, data: ProductUpdate, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(producto, key, value)
    session.commit()
    session.refresh(producto)
    return producto

@router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.activo = False
    session.commit()
    return {"message": "Producto desactivado correctamente"}

@router.put("/productos/{producto_id}/comprar", response_model=ProductRead)
def comprar_producto(producto_id: int, cantidad: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if cantidad <= 0:
        raise HTTPException(status_code=400, detail="Cantidad inválida")
    if producto.cantidad < cantidad:
        raise HTTPException(status_code=400, detail="No hay suficiente stock disponible.")
    producto.cantidad -= cantidad
    session.commit()
    session.refresh(producto)
    return producto