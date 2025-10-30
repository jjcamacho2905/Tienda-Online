from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import init_db, get_session
from modelos import Categoria, Producto
from Esquemas import CategoryCreate, CategoryRead, CategoryUpdate, ProductCreate, ProductRead, ProductUpdate
from typing import Optional, List
from fastapi.responses import JSONResponse



app = FastAPI(title="Sistema de Tienda Online", version="2.0")



# INICIO DE LA BASE DE DATOS

@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "API de Tienda Online operativa"}



# CRUD DE CATEGORÍAS

@app.post("/categorias", response_model=CategoryRead)
def crear_categoria(datos: CategoryCreate, session: Session = Depends(get_session)):
    if len(datos.nombre.strip()) < 3:
        raise HTTPException(status_code=400, detail="El nombre de la categoría es muy corto.")
    if session.exec(select(Categoria).where(Categoria.nombre == datos.nombre)).first():
        raise HTTPException(status_code=404, detail="La categoría ya existe.")
    categoria = Categoria.from_orm(datos)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return JSONResponse(status_code=201, content=categoria.dict())

@app.get("/categorias", response_model=List[CategoryRead])
def listar_categorias(session: Session = Depends(get_session)):
    return session.exec(select(Categoria)).all()

@app.get("/categorias/{id_categoria}", response_model=CategoryRead)
def obtener_categoria(id_categoria: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@app.put("/categorias/{id_categoria}", response_model=CategoryRead)
def actualizar_categoria(id_categoria: int, datos: CategoryUpdate, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if datos.nombre and len(datos.nombre.strip()) < 3:
        raise HTTPException(status_code=400, detail="El nombre es muy corto.")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(categoria, key, value)
    session.commit()
    session.refresh(categoria)
    return categoria

@app.delete("/categorias/{id_categoria}")
def eliminar_categoria(id_categoria: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    productos = session.exec(select(Producto).where(Producto.categoria_id == id_categoria)).all()
    if productos:
        raise HTTPException(status_code=404, detail="No se puede eliminar, tiene productos asociados.")
    session.delete(categoria)
    session.commit()
    return {"mensaje": "Categoría eliminada correctamente"}


# CRUD DE PRODUCTOS

@app.post("/productos", response_model=ProductRead)
def crear_producto(datos: ProductCreate, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, datos.categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    if datos.cantidad < 0:
        raise HTTPException(status_code=400, detail="La cantidad no puede ser negativa.")
    if datos.precio <= 0:
        raise HTTPException(status_code=400, detail="El precio debe ser mayor que 0.")
    producto = Producto.from_orm(datos)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return JSONResponse(status_code=201, content=producto.dict())

@app.get("/productos", response_model=List[ProductRead])
def listar_productos(session: Session = Depends(get_session)):
    consulta = select(Producto)
    productos = session.exec(consulta).all()
    return productos

@app.get("/productos/{id_producto}", response_model=ProductRead)
def obtener_producto(id_producto: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/productos/{id_producto}", response_model=ProductRead)
def actualizar_producto(id_producto: int, datos: ProductUpdate, session: Session = Depends(get_session)):
    producto = session.get(Producto, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if datos.cantidad is not None and datos.cantidad < 0:
        raise HTTPException(status_code=400, detail="La cantidad no puede ser negativa.")
    if datos.precio is not None and datos.precio <= 0:
        raise HTTPException(status_code=400, detail="El precio debe ser mayor que 0.")
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(producto, key, value)
    session.commit()
    session.refresh(producto)
    return producto

@app.delete("/productos/{id_producto}")
def eliminar_producto(id_producto: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()
    return {"mensaje": "Producto eliminado correctamente"}

@app.put("/productos/{id_producto}/comprar", response_model=ProductRead)
def comprar_producto(id_producto: int, cantidad: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if producto.cantidad < cantidad:
        raise HTTPException(status_code=400, detail="No hay suficiente stock.")
    producto.cantidad -= cantidad
    session.commit()
    session.refresh(producto)
    return producto

@app.put("/productos/{id_producto}/estado", response_model=ProductRead)
def cambiar_estado_producto(id_producto: int, activo: bool, session: Session = Depends(get_session)):
    producto = session.get(Producto, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.activo = activo
    session.commit()
    session.refresh(producto)
    return producto