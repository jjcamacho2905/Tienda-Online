# API Tienda Online

Este proyecto es una API hecha con FastAPI para manejar una tienda básica.
Se pueden crear y administrar categorías y productos, y cada categoría puede tener varios productos asociados.
También tiene opciones para activar o desactivar registros sin borrarlos del todo

---

## Qué hace esta API
- Permite crear, listar y borrar productos y categorías.
- Las categorías pueden tener varios productos.
- Los productos se pueden activar o desactivar sin eliminarl

---

##  Tecnologías utilizadas

- Python 3.10+
- FastAPI
- SQLModel
- SQLite
- Uvicorn

---

##  Instalación y configuración

### 1️ Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/tienda-fastapi.git
cd tienda-fastapi
2 Crear entorno virtual
bash
Copiar código
python -m venv .venv
3️  Activar entorno
Windows:

bash
Copiar código
.venv\Scripts\activate
Linux/Mac:

bash
Copiar código
source .venv/bin/activate
4 Instalar dependencias
bash
Copiar código
pip install -r requirements.txt
5️  Crear archivo .env
bash
Copiar código
cp .env.example .env

Estructura del proyecto

   main.py

Archivo principal de la aplicación.

Inicializa la API FastAPI

Carga la base de datos al iniciar (on_startup)

Define los endpoints principales (categorías y productos)

Ejecuta el servidor con uvicorn main:app --reload

   rutas.py

Contiene los endpoints organizados por recursos:

Rutas para categorías (/categorias)

Rutas para productos (/productos)

Lógica CRUD (GET, POST, PUT, DELETE)

Implementa validaciones de negocio (stock, categorías, duplicados, etc.)

   database.py

Encargado de la configuración de la base de datos y la sesión:

Carga variables de entorno (.env)

Define el motor de base de datos (create_engine)

Funciones para inicializar (init_db) y obtener sesión (get_session)

    modelos.py

Define las tablas y relaciones de la base de datos usando SQLModel:

Categoria → tabla de categorías

Producto → tabla de productos (relacionada con Categoria mediante categoria_id)

    Esquemas.py

Define los modelos Pydantic para validar datos de entrada/salida:

CategoryCreate, CategoryRead, CategoryUpdate

ProductCreate, ProductRead, ProductUpdate

Controlan las reglas de negocio y validaciones de cada campo (nombre, precio, cantidad, etc.)
   
   
tienda-fastapi/
 ┣ main.py
 ┣ modelos.py
 ┣ esquemas.py
 ┣ rutas_productos.py
 ┣ rutas_categorias.py
 ┣ database.py
 ┣ requirements.txt
 ┣ .env.example
 ┗ README.md

 Modelos principales

 Categoría
Campo	Tipo	Descripción
id	int	Identificador único
nombre	str	Nombre de la categoría
descripcion	str	Descripción opcional

 Producto
Campo	   Tipo	         Descripción
id	        int       	Identificador único
nombre	    str	        Nombre del producto
precio	    float	      Precio unitario
cantidad	int	           Stock disponible
activo	    bool	    Estado (True = activo, False = inactivo)
categoria_id int	    ID de la categoría asociada

  Ejecución del servidor

uvicorn main:app --reload

 
 Endpoints disponibles
Método	  Endpoint     	                     Descripción
GET	      /categorias	                    Listar categorías
POST	  /categorias	                    Crear categoría
PUT	      /categorias/{id}	                Actualizar categoría
DELETE	  /categorias/{id}	                Eliminar categoría
GET	      /productos	                    Listar productos
POST	  /productos	                    Crear producto
PUT	      /productos/{producto_id}	        Actualizar producto
DELETE	  /productos/{producto_id}	        Eliminar producto
PUT      /productos/{producto_id}/estado	Activar/Desactivar producto
PUT	     /productos/{producto_id}/comprar	Restar stock (evita negativos)
GET	     /productos/estado	                 Listar productos por estado

   Ejemplos de respuestas
GET /
json
Copiar código
{
  "mensaje": "API de Tienda Online operativa"
}
POST /categorias
Body:

json
Copiar código
{ "nombre": "Electrónica" }
Respuestas:

  201 → Categoría creada

  400 → Nombre muy corto

  409 → La categoría ya existe

PUT /productos/{id}/comprar?cantidad=3
Respuestas:

   200 → Stock reducido correctamente

   400 → No hay suficiente stock

   404 → Producto no encontrado

