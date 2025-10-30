from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import init_db, get_session, motor
from modelos import Categoria, Producto
from Esquemas import CategoryCreate, CategoryRead, CategoryUpdate, ProductCreate, ProductRead, ProductUpdate

app = FastAPI(title="Sistema de Tienda Online", version="2.0")


# INICIO
@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "API de Tienda Online operativa"}


# CRUD DE CATEGORÍAS

@app.post("/categorias", response_model=CategoryRead)
def crear_categoria(data: CategoryCreate, session: Session = Depends(get_session)):
    categoria = Categoria.from_orm(data)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


@app.get("/categorias", response_model=list[CategoryRead])
def listar_categorias(session: Session = Depends(get_session)):
    return session.exec(select(Categoria).where(Categoria.activo == True)).all()


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
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


@app.delete("/categorias/{id}")
def eliminar_categoria(id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    categoria.activo = False  # Desactivar en lugar de eliminar
    session.commit()
    return {"message": "Categoría desactivada correctamente"}


# CRUD DE PRODUCTOS

@app.post("/productos", response_model=ProductRead)
def crear_producto(producto: ProductCreate, session: Session = Depends(get_session)):
    # Validación de stock no negativo
    if producto.stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo.")

    categoria = session.get(Categoria, producto.categoria_id)
    if not categoria:
        raise HTTPException(status_code=400, detail="La categoría no existe.")

    producto_db = Producto.from_orm(producto)
    session.add(producto_db)
    session.commit()
    session.refresh(producto_db)
    return producto_db


@app.get("/productos", response_model=list[ProductRead])
def listar_productos(stock: Optional[int] = None, precio: Optional[float] = None, categoria_id: Optional[int] = None,
                     session: Session = Depends(get_session)):
    query = select(Producto)

    if stock is not None:
        query = query.where(Producto.stock >= stock)
    if precio is not None:
        query = query.where(Producto.precio <= precio)
    if categoria_id is not None:
        query = query.where(Producto.categoria_id == categoria_id)

    productos = session.exec(query).all()
    return productos


@app.get("/productos/{producto_id}", response_model=ProductRead)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@app.put("/productos/{producto_id}", response_model=ProductRead)
def actualizar_producto(producto_id: int, nuevo_producto: ProductUpdate, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Validación de stock no negativo
    if nuevo_producto.stock is not None and nuevo_producto.stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo.")

    for key, value in nuevo_producto.dict(exclude_unset=True).items():
        setattr(producto, key, value)

    session.commit()
    session.refresh(producto)
    return producto


@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.activo = False  # Desactivar en lugar de eliminar
    session.commit()
    return {"message": "Producto desactivado correctamente"}


# Endpoint para restar stock al comprar producto
@app.put("/productos/{producto_id}/comprar", response_model=ProductRead)
def restar_stock(producto_id: int, cantidad: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if producto.stock < cantidad:
        raise HTTPException(status_code=400, detail="No hay suficiente stock disponible.")

    producto.stock -= cantidad
    session.commit()
    session.refresh(producto)
    return producto