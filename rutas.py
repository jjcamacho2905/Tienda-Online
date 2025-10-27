from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import motor
from modelos import Categoria, Producto

router = APIRouter()

#Endpoints de categoria

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