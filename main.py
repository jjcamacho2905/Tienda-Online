from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import init_db, get_session
from modelos import Categoria, Producto
from Esquemas import CategoryCreate, CategoryRead, CategoryUpdate, ProductCreate, ProductRead, ProductUpdate
from typing import Optional, List
from fastapi.responses import JSONResponse

# Inicialización de la aplicación FastAPI

app = FastAPI(title="Sistema de Tienda Online", version="2.0")



# INICIO DE LA BASE DE DATOS


@app.on_event("startup")
def on_startup():
    """
    Evento que se ejecuta al iniciar la aplicación.
    Inicializa la base de datos mediante la función `init_db()`.
    """
    init_db()  # Crea las tablas si no existen


@app.get("/")
def root():
    """
    Endpoint raíz de la API.

    Returns:
        dict: Mensaje de confirmación de que la API está operativa.
    """
    return {"message": "API del Sistema de Gestión de Tienda Online operativa"}



# CRUD DE CATEGORÍAS


@app.post("/categorias", response_model=CategoryRead)
def crear_categoria(datos: CategoryCreate, session: Session = Depends(get_session)):
    """
    Crea una nueva categoría en la base de datos.

    Args:
        datos (CategoryCreate): Datos de la categoría (nombre).
        session (Session): Sesión de base de datos inyectada.

    Raises:
        HTTPException 409: Si el nombre de la categoría ya existe.

    Returns:
        JSONResponse: Categoría creada con código de estado 201.
    """
    ## Validar nombre único
    if session.exec(select(Categoria).where(Categoria.nombre == datos.nombre)).first():
        raise HTTPException(status_code=409, detail="La categoría ya existe.")
    ## Crear instancia y activar categoría
    categoria = Categoria.from_orm(datos)
    categoria.activo = True
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return JSONResponse(status_code=201, content=categoria.dict())  # Retorna código 201 (creado)


@app.get("/categorias", response_model=List[CategoryRead])
def listar_categorias(session: Session = Depends(get_session)):
    """
    Lista todas las categorías activas.

    Returns:
        list: Lista de categorías activas (status 200).
    """
    # Solo retorna las categorías activas
    return session.exec(select(Categoria).where(Categoria.activo == True)).all()


@app.get("/categorias/{id_categoria}", response_model=CategoryRead)
def obtener_categoria(id_categoria: int, session: Session = Depends(get_session)):
    """
    Obtiene una categoría por su ID.
    """
    # Busca la categoría en la BD
    categoria = session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@app.put("/categorias/{id_categoria}", response_model=CategoryRead)
def actualizar_categoria(id_categoria: int, datos: CategoryUpdate, session: Session = Depends(get_session)):
    """
    Actualiza los datos de una categoría existente.
    """
    categoria = session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    # Actualiza solo los campos enviados (exclude_unset evita reemplazar con None)
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(categoria, key, value)
    session.commit()
    session.refresh(categoria)
    return categoria


@app.delete("/categorias/{id_categoria}")
def eliminar_categoria(id_categoria: int, session: Session = Depends(get_session)):
    """
    Elimina una categoría si no tiene productos asociados.
    """
    categoria = session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Verifica si existen productos relacionados
    productos = session.exec(select(Producto).where(Producto.categoria_id == id_categoria)).all()
    if productos:
        raise HTTPException(status_code=400, detail="No se puede eliminar, tiene productos asociados.")

    session.delete(categoria)
    session.commit()
    return {"mensaje": "Categoría eliminada correctamente"}


@app.get("/categorias/{id_categoria}/productos", response_model=CategoryRead)
def categoria_con_productos(id_categoria: int, session: Session = Depends(get_session)):
    """
    Obtiene una categoría junto con sus productos relacionados.
    """
    categoria = session.get(Categoria, id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


# CRUD DE PRODUCTOS


@app.post("/productos", response_model=ProductRead)
def crear_producto(datos: ProductCreate, session: Session = Depends(get_session)):
    """
    Crea un nuevo producto.
    """
    # Verificar si la categoría existe
    categoria = session.get(Categoria, datos.categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Validaciones de cantidad y precio
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
def listar_productos(
    stock_min: Optional[int] = Query(None, description="Stock mínimo"),
    precio_max: Optional[float] = Query(None, description="Precio máximo"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    session: Session = Depends(get_session)
):
    """
    Lista productos con filtros opcionales.
    """
    # Construye la consulta dinámicamente según los filtros
    consulta = select(Producto)
    if stock_min is not None:
        consulta = consulta.where(Producto.cantidad >= stock_min)
    if precio_max is not None:
        consulta = consulta.where(Producto.precio <= precio_max)
    if categoria_id is not None:
        consulta = consulta.where(Producto.categoria_id == categoria_id)

    return session.exec(consulta).all()


@app.get("/productos/{id_producto}", response_model=ProductRead)
def obtener_producto(id_producto: int, session: Session = Depends(get_session)):
    """
    Obtiene un producto por su ID.
    """
    producto = session.get(Producto, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@app.get("/productos/{id_producto}/categoria", response_model=ProductRead)
def producto_con_categoria(id_producto: int, session: Session = Depends(get_session)):
    """
    Obtiene un producto junto con su categoría asociada.
    """
    producto = session.get(Producto, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Agrega los datos de la categoría al resultado
    categoria = session.get(Categoria, producto.categoria_id)
    resultado = producto.dict()
    resultado["categoria"] = {"id": categoria.id, "nombre": categoria.nombre}
    return resultado


@app.put("/productos/{id_producto}", response_model=ProductRead)
def actualizar_producto(id_producto: int, datos: ProductUpdate, session: Session = Depends(get_session)):
    """
    Actualiza los datos de un producto existente.
    """
    producto = session.get(Producto, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Validaciones
    if datos.cantidad is not None and datos.cantidad < 0:
        raise HTTPException(status_code=400, detail="La cantidad no puede ser negativa.")
    if datos.precio is not None and datos.precio <= 0:
        raise HTTPException(status_code=400, detail="El precio debe ser mayor que 0.")

    # Actualiza solo los campos enviados
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(producto, key, value)
    session.commit()
    session.refresh(producto)
    return producto


@app.delete("/productos/{id_producto}")
def eliminar_producto(id_producto: int, session: Session = Depends(get_session)):
    """
    Elimina un producto por ID.
    """
    producto = session.get(Producto, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()
    return {"mensaje": "Producto eliminado correctamente"}


@app.put("/productos/{id_producto}/comprar", response_model=ProductRead)
def comprar_producto(id_producto: int, cantidad: int, session: Session = Depends(get_session)):
    """
    Resta stock de un producto al realizar una compra.
    """
    producto = session.get(Producto, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Validaciones de cantidad
    if cantidad <= 0:
        raise HTTPException(status_code=400, detail="Cantidad inválida")
    if producto.cantidad < cantidad:
        raise HTTPException(status_code=400, detail="No hay suficiente stock")

    producto.cantidad -= cantidad  # Resta la cantidad comprada
    session.commit()
    session.refresh(producto)
    return producto


@app.put("/productos/{id_producto}/estado", response_model=ProductRead)
def cambiar_estado_producto(id_producto: int, activo: bool, session: Session = Depends(get_session)):
    """
    Activa o desactiva un producto.
    """
    producto = session.get(Producto, id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto.activo = activo  # Cambia el estado activo/inactivo
    session.commit()
    session.refresh(producto)
    return producto
