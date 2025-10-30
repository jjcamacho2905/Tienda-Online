#  API Tienda Online

API REST creada con **FastAPI** y **SQLModel** para gestionar una tienda en línea.  
Permite administrar **categorías** y **productos**, con operaciones completas CRUD (crear, leer, actualizar y eliminar).

---

##  Características principales

- CRUD completo para **categorías** y **productos**
- Relación uno a muchos entre **categoría → productos**
- Control de **estado activo/inactivo** (sin eliminar físicamente)
- Validación para **evitar stock negativo**
- Filtros opcionales para listar productos por **stock, precio o categoría**
- Base de datos ligera: `tienda.db` (SQLite)

---

##  Tecnologías utilizadas

- Python 3.10+
- FastAPI
- SQLModel
- SQLite
- Uvicorn

---

##  Instalación y configuración

### 1️. Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/tienda-fastapi.git
cd tienda-fastapi

## 2 
Crear entorno virtual
python -m venv .venv

3️  Activar entorno️ 
Linux:

source .venv/bin/activate

4  Instalar dependencias
pip install -r requirements.txt

5️ Crear archivo .env (a partir del ejemplo)
.env.example .env

6. Estructura del proyecto
     tienda-fastapi
 ┣  main.py                  
 ┣  modelos.py             
 ┣  esquemas.py              
 ┣  rutas_productos.py       
 ┣  rutas_categorias.py      
 ┣  database.py              
 ┣  requirements.txt         
 ┣  .env.example            
 ┗  README.md                






7. Modelos principales:

##Categorias
 
 Campo        Tipo  Descripción            
 id           int   Identificador único    
 nombre       str   Nombre de la categoría 
 descripcion  str   Descripción opcional   

##Producto

 Campo         Tipo   Descripción                                 
 id            int    Identificador único                                   
 nombre        str    Nombre del producto                                   
 precio        float  Precio unitario                                       
 cantidad      int    Stock disponible                                      
 activo        bool   Estado del producto (True = activo, False = inactivo) 
 categoria_id  int    ID de la categoría asociada   
 
## 8. Ejecución del servidor

Inicia el servidor con:
uvicorn main:app --reload

##9. Endpoints disponibles
 
 Método     Endpoint                              Descripción                    |

 GET       `/categorias`                        Listar categorías              |
 POST      `/categorias`                        Crear categoría                |
 PUT       `/categorias/{id}`                   Actualizar categoría           |
 DELETE    `/categorias/{id}`                   Eliminar categoría             |
 GET       `/productos`                         Listar productos               |
 POST      `/productos`                         Crear producto                 |
 PUT       `/productos/{producto_id}`           Actualizar producto            |
 DELETE    `/productos/{producto_id}`           Eliminar producto              |
 PUT       `/productos/{producto_id}/estado`    Activar/Desactivar producto    |
 PUT       `/productos/{producto_id}/comprar`   Restar stock (evita negativos) |
 GET       `/productos/estado`                  Listar productos por estado    |
