#  API Tienda Online

API REST creada con **FastAPI** y **SQLModel** para gestionar una tienda en línea.  
Permite administrar **categorías** y **productos**, con operaciones completas CRUD (crear, leer, actualizar y eliminar).

---

##  Tecnologías utilizadas

- **Python 3.12+**
- **FastAPI** – Framework backend moderno y rápido
- **SQLModel** – ORM para manejar bases de datos SQL
- **Uvicorn** – Servidor ASGI para ejecutar la API
- **Pydantic** – Validación de datos
- **SQLite** – Base de datos ligera local
- **Python-dotenv** – Manejo de variables de entorno desde `.env`

---

##  Estructura del proyecto

- **main.py** → Punto de entrada principal de la API  
- **database.py** → Configuración del motor y sesión de base de datos  
- **modelos.py** → Modelos SQLModel de Producto y Categoría  
- **schemas.py** → Esquemas Pydantic para validación  
- **rutas.py** → Rutas separadas por categorías y productos  
- **.env** → Variables de entorno (configuración de la base de datos y entorno)  
- **requirements.txt** → Dependencias del proyecto  
- **README.md** → Este archivo  

