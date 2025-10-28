from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import motor
from modelos import Categoria, Producto

router = APIRouter()


# ENDPOINTS DE CATEGORÍAS


@router.post("/categorias")
def crear_categoria(categoria: Categoria):
    with Session(motor) as session:
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return categoria


@router.get("/categorias")
def listar_categorias():
    with Session(motor) as session:
        categorias = session.exec(select(Categoria).where(Categoria.activa == True)).all()
        return categorias


@router.put("/categorias/{categoria_id}")
def actualizar_categoria(categoria_id: int, nueva_categoria: Categoria):
    with Session(motor) as session:
        categoria = session.get(Categoria, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        categoria.nombre = nueva_categoria.nombre
        categoria.descripcion = nueva_categoria.descripcion
        categoria.activa = nueva_categoria.activa
        session.commit()
        session.refresh(categoria)
        return categoria


@router.delete("/categorias/{categoria_id}")
def desactivar_categoria(categoria_id: int):
    with Session(motor) as session:
        categoria = session.get(Categoria, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        categoria.activa = False
        session.commit()
        return {"mensaje": "Categoría desactivada correctamente"}


# ENDPOINTS DE PRODUCTOS


@router.post("/productos")
def crear_producto(producto: Producto):
    if producto.stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo")

    with Session(motor) as session:
        session.add(producto)
        session.commit()
        session.refresh(producto)
        return producto


@router.get("/productos")
def listar_productos():
    with Session(motor) as session:
        return session.exec(select(Producto)).all()


@router.get("/productos/categoria/{categoria_id}")
def productos_por_categoria(categoria_id: int):
    with Session(motor) as session:
        productos = session.exec(select(Producto).where(Producto.categoria_id == categoria_id)).all()
        return productos


@router.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, nuevo_producto: Producto):
    with Session(motor) as session:
        producto = session.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        if nuevo_producto.stock < 0:
            raise HTTPException(status_code=400, detail="El stock no puede ser negativo")
        producto.nombre = nuevo_producto.nombre
        producto.precio = nuevo_producto.precio
        producto.stock = nuevo_producto.stock
        producto.categoria_id = nuevo_producto.categoria_id
        session.commit()
        session.refresh(producto)
        return producto


@router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    with Session(motor) as session:
        producto = session.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        session.delete(producto)
        session.commit()
        return {"mensaje": "Producto eliminado correctamente"}


@router.post("/productos/{producto_id}/restock")
def aumentar_stock(producto_id: int, cantidad: int):
    with Session(motor) as session:
        producto = session.get(Producto, producto_id)
        if producto:
            producto.stock += cantidad
            session.commit()
            session.refresh(producto)
            return producto
        else:
            raise HTTPException(status_code=404, detail="Producto no encontrado")


@router.post("/productos/{producto_id}/purchase")
def comprar_producto(producto_id: int, cantidad: int):
    with Session(motor) as session:
        producto = session.get(Producto, producto_id)
        if producto:
            if producto.stock < cantidad:
                raise HTTPException(status_code=400, detail="Stock insuficiente")
            producto.stock -= cantidad
            session.commit()
            session.refresh(producto)
            return producto
        else:
            raise HTTPException(status_code=404, detail="Producto no encontrado")