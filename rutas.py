from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import motor
from modelos import Categoria, Producto

router = APIRouter()

# --- CATEGORÍAS ---
@router.post("/categorias", tags=["Categorías"])
def crear_categoria(categoria: Categoria):
    with Session(motor) as session:
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return categoria

@router.get("/categorias", tags=["Categorías"])
def listar_categorias():
    with Session(motor) as session:
        return session.exec(select(Categoria)).all()

@router.get("/categorias/{categoria_id}", tags=["Categorías"])
def obtener_categoria(categoria_id: int):
    with Session(motor) as session:
        categoria = session.get(Categoria, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return categoria

@router.put("/categorias/{categoria_id}", tags=["Categorías"])
def actualizar_categoria(categoria_id: int, nueva_categoria: Categoria):
    with Session(motor) as session:
        categoria = session.get(Categoria, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        categoria.nombre = nueva_categoria.nombre
        categoria.descripcion = nueva_categoria.descripcion
        session.commit()
        session.refresh(categoria)
        return categoria

@router.delete("/categorias/{categoria_id}", tags=["Categorías"])
def eliminar_categoria(categoria_id: int):
    with Session(motor) as session:
        categoria = session.get(Categoria, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        session.delete(categoria)
        session.commit()
        return {"mensaje": "Categoría eliminada correctamente"}


# --- PRODUCTOS ---
@router.post("/productos", tags=["Productos"])
def crear_producto(producto: Producto):
    with Session(motor) as session:
        session.add(producto)
        session.commit()
        session.refresh(producto)
        return producto

@router.get("/productos", tags=["Productos"])
def listar_productos():
    with Session(motor) as session:
        return session.exec(select(Producto)).all()

@router.get("/productos/{producto_id}", tags=["Productos"])
def obtener_producto(producto_id: int):
    with Session(motor) as session:
        producto = session.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto

@router.put("/productos/{producto_id}", tags=["Productos"])
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

@router.delete("/productos/{producto_id}", tags=["Productos"])
def eliminar_producto(producto_id: int):
    with Session(motor) as session:
        producto = session.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        session.delete(producto)
        session.commit()
        return {"mensaje": "Producto eliminado correctamente"}
