from fastapi import FastAPI, Depends
from sqlmodel import Session
from app.database import init_db, get_session
from app.schemas import *
from app.crud import category, product

app = FastAPI(title="Sistema de Tienda Online", version="2.0")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "API de Tienda Online operativa"}

# --- Categorías ---
@app.post("/categorias", response_model=CategoryRead)
def crear_categoria(data: CategoryCreate, session: Session = Depends(get_session)):
    return category.create_category(session, data)

@app.get("/categorias", response_model=list[CategoryRead])
def listar_categorias(session: Session = Depends(get_session)):
    return category.list_categories(session)

@app.get("/categorias/{id}", response_model=CategoryRead)
def obtener_categoria(id: int, session: Session = Depends(get_session)):
    return category.get_category(session, id)

@app.put("/categorias/{id}", response_model=CategoryRead)
def actualizar_categoria(id: int, data: CategoryUpdate, session: Session = Depends(get_session)):
    return category.update_category(session, id, data)

@app.delete("/categorias/{id}")
def eliminar_categoria(id: int, session: Session = Depends(get_session)):
    return category.delete_category(session, id)

# --- Productos ---
@app.post("/productos", response_model=ProductRead)
def crear_producto(data: ProductCreate, session: Session = Depends(get_session)):
    return product.create_product(session, data)

@app.get("/productos", response_model=list[ProductRead])
def listar_productos(session: Session = Depends(get_session)):
    return product.list_products(session)

@app.get("/productos/categoria/{id}", response_model=list[ProductRead])
def obtener_productos_por_categoria(id: int, session: Session = Depends(get_session)):
    return product.get_product_by_category(session, id)

@app.put("/productos/{id}", response_model=ProductRead)
def actualizar_producto(id: int, data: ProductUpdate, session: Session = Depends(get_session)):
    return product.update_product(session, id, data)

@app.delete("/productos/{id}")
def eliminar_producto(id: int, session: Session = Depends(get_session)):
    return product.delete_product(session, id)

@app.post("/productos/{id}/restock", response_model=ProductRead)
def restock_producto(id: int, cantidad: int, session: Session = Depends(get_session)):
    return product.restock_product(session, id, cantidad)

@app.post("/productos/{id}/purchase", response_model=ProductRead)
def comprar_producto(id: int, cantidad: int, session: Session = Depends(get_session)):
    return product.purchase_product(session, id, cantidad)