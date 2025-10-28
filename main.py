from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from database import init_db, get_session
from modelos import Category
from schemas import CategoryCreate, CategoryRead, CategoryUpdate

app = FastAPI(title="Sistema de Tienda Online", version="2.0")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "API de Tienda Online operativa"}

# --- CRUD de Categorías ---

@app.post("/categorias", response_model=CategoryRead)
def crear_categoria(data: CategoryCreate, session: Session = Depends(get_session)):
    categoria = Category.from_orm(data)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

@app.get("/categorias", response_model=list[CategoryRead])
def listar_categorias(session: Session = Depends(get_session)):
    return session.query(Category).all()

@app.get("/categorias/{id}", response_model=CategoryRead)
def obtener_categoria(id: int, session: Session = Depends(get_session)):
    categoria = session.get(Category, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@app.put("/categorias/{id}", response_model=CategoryRead)
def actualizar_categoria(id: int, data: CategoryUpdate, session: Session = Depends(get_session)):
    categoria = session.get(Category, id)
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
    categoria = session.get(Category, id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    session.delete(categoria)
    session.commit()
    return {"message": "Categoría eliminada correctamente"}