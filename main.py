from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import init_db, get_session
from modelos import Categoria, Producto
from Esquemas import CategoryCreate, CategoryRead, CategoryUpdate, ProductCreate, ProductRead, ProductUpdate
from typing import Optional, List


app = FastAPI(title="Sistema de Tienda Online", version="2.0")


# ==========================
# INICIO DE LA BASE DE DATOS
# ==========================
@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "API de Tienda Online operativa"}


# ==========================
# CRUD DE CATEGORÍAS
# ==========================

@app.post("/categorias", response_model=CategoryRead)
def crear_categoria(data: CategoryCreate, session: Session = Depends(get_session)):
    categoria_existente = session.exec(select(Categoria).where(Categoria.nombre == data.nombre)).first()
    if categoria_existente:
        raise HTTPException(status_code=400, detail="El nombre de la categoría debe ser único.")

    categoria = Categoria.from_orm(data)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


@app.get("/categorias", response_model=list[CategoryRead])
def listar_categorias(session: Session = Depends(get_session)):
    return session.exec(select(Categoria)).all()


@app.get("/categorias/{id}", response_model=CategoryRead)
def obtener_categoria(id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@app.put("/categorias/{id}", response_model=CategoryRead)
def actualizar_categoria(id: int, data: CategoryUpdate, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(categoria, key, value)

    session.commit()
    session.refresh(categoria)
    return categoria


@app.delete("/categorias/{id}")
def eliminar_categoria(id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    session.delete(categoria)
    session.commit()
    return {"message": "Categoría eliminada correctamente"}


# ==========================
# CRUD DE PRODUCTOS
# ==========================

@app.post("/productos", response_model=ProductRead)
def crear_producto(data: ProductCreate, session: Session = Depends(get_session)):
    categoria = session.exec(select(Categoria).where(Categoria.id == data.categoria_id)).first()
    if not categoria:
        raise HTTPException(status_code=400, detail="La categoría asignada no existe.")

    if data.cantidad < 0:
        raise HTTPException(status_code=400, detail="La cantidad no puede ser negativa.")

    producto = Producto.from_orm(data)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@app.get("/productos", response_model=list[ProductRead])
def listar_productos(
    stock_min: Optional[int] = None,
    precio_max: Optional[float] = None,
    categoria_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    query = select(Producto)
    if stock_min is not None:
        query = query.where(Producto.cantidad >= stock_min)
    if precio_max is not None:
        query = query.where(Producto.precio <= precio_max)
    if categoria_id is not None:
        query = query.where(Producto.categoria_id == categoria_id)

    return session.exec(query).all()


@app.get("/productos/{producto_id}", response_model=ProductRead)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@app.put("/productos/{producto_id}", response_model=ProductRead)
def actualizar_producto(producto_id: int, data: ProductUpdate, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if data.cantidad is not None and data.cantidad < 0:
        raise HTTPException(status_code=400, detail="La cantidad no puede ser negativa.")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(producto, key, value)

    session.commit()
    session.refresh(producto)
    return producto


@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    session.delete(producto)
    session.commit()
    return {"message": "Producto eliminado correctamente"}


@app.put("/productos/{producto_id}/comprar", response_model=ProductRead)
def restar_stock(producto_id: int, cantidad: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if producto.cantidad < cantidad:
        raise HTTPException(status_code=400, detail="No hay suficiente stock disponible.")

    producto.cantidad -= cantidad
    session.commit()
    session.refresh(producto)
    return producto
@app.get("/productos/estado", response_model=List[ProductRead])
def listar_productos_por_estado(
    activo: bool = Query(True, description="Filtrar productos activos (True) o inactivos (False)"),
    session: Session = Depends(get_session),
):
    productos = session.exec(select(Producto).where(Producto.activo == activo)).all()
    return productos


@app.put("/productos/{producto_id}/estado", response_model=ProductRead)
def cambiar_estado_producto(producto_id: int, activo: bool, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto.activo = activo
    session.commit()
    session.refresh(producto)
    return producto