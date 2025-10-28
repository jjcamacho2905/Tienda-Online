from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import init_db, get_session, motor
from modelos import Categoria, Producto
from schemas import CategoryCreate, CategoryRead, CategoryUpdate

app = FastAPI(title="Sistema de Tienda Online", version="2.0")

#INICIO
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "API de Tienda Online operativa"}


#CRUD DE CATEGORÍAS


@app.post("/categorias", response_model=CategoryRead)
def crear_categoria(data: CategoryCreate, session: Session = Depends(get_session)):
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
    session.add(categoria)
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


#CRUD DE PRODUCTOS


@app.post("/productos")
def crear_producto(producto: Producto):
    with Session(motor) as session:
        session.add(producto)
        session.commit()
        session.refresh(producto)
        return producto

@app.get("/productos")
def listar_productos():
    with Session(motor) as session:
        return session.exec(select(Producto)).all()

@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int):
    with Session(motor) as session:
        producto = session.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto

@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, nuevo_producto: Producto):
    with Session(motor) as session:
        producto = session.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        producto.nombre = nuevo_producto.nombre
        producto.precio = nuevo_producto.precio
        producto.cantidad = nuevo_producto.cantidad
        producto.categoria_id = nuevo_producto.categoria_id
        session.commit()
        session.refresh(producto)
        return producto

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    with Session(motor) as session:
        producto = session.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        session.delete(producto)
        session.commit()
        return {"mensaje": "Producto eliminado correctamente"}
