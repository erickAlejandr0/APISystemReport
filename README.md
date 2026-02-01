# API System Report

API REST geoespacial desarrollada con **FastAPI** para la gestión de reportes de incidentes con soporte para datos GeoJSON. Diseñada para sistemas de monitoreo y reporte ciudadano con capacidades de geolocalización.

##  Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Estructura del Proyecto](#-estructura-del-proyecto)


## Características

- **Sistema de autenticación de usuarios** - Registro e inicio de sesión
- **Soporte GeoJSON** - Manejo de datos geoespaciales con validación de geometrías
- **Gestión de reportes** - Crear y categorizar reportes de incidentes
- **Capas geográficas** - Consulta de provincias, distritos, corregimientos y reportes
- **Alto rendimiento** - Pool de conexiones asíncronas con asyncpg
- **CORS habilitado** - Listo para integrarse con frontends

## Tecnologías

| Tecnología | Versión | Descripción |
|------------|---------|-------------|
| [FastAPI](https://fastapi.tiangolo.com/) | 0.115.12 | Framework web moderno y de alto rendimiento |
| [Uvicorn](https://www.uvicorn.org/) | 0.34.2 | Servidor ASGI para producción |
| [Gunicorn](https://gunicorn.org/) | - | Servidor WSGI para despliegue |
| [asyncpg](https://github.com/MagicStack/asyncpg) | 0.30.0 | Driver PostgreSQL asíncrono |
| [Pydantic](https://docs.pydantic.dev/) | 2.11.4 | Validación de datos |
| [geojson-pydantic](https://github.com/developmentseed/geojson-pydantic) | 2.0.0 | Modelos GeoJSON |

## Requisitos Previos

- Python 3.10+
- PostgreSQL con extensión PostGIS
- pip o pipenv

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/erickAlejandr0/APISystemReport.git
cd APISystemReport
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

La aplicación utiliza variables de entorno para la configuración de la base de datos. Puedes configurarlas de las siguientes formas:

### Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `PG_USER` | Usuario de PostgreSQL | `postgres` |
| `PG_PASS` | Contraseña de PostgreSQL | `1234` |
| `PG_DB` | Nombre de la base de datos | `Panama` |
| `PG_HOST` | Host de la base de datos | `localhost` |
| `PG_PORT` | Puerto de PostgreSQL | `5432` |

### Archivo .env (recomendado)

Crea un archivo `.env` en la raíz del proyecto:

```env
PG_USER=tu_usuario
PG_PASS=tu_contraseña
PG_DB=nombre_base_datos
PG_HOST=localhost
PG_PORT=5432
```

## Uso

### Desarrollo

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Producción

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Acceder a la documentación

Una vez ejecutada la API, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints de la API

### Usuarios (`/usuarios`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/usuarios/registrar` | Registrar nuevo usuario |
| `POST` | `/usuarios/autenticar` | Autenticar usuario existente |

#### Ejemplo: Registrar usuario

```json
POST /usuarios/registrar
{
  "nombre": "Juan",
  "apellido": "Pérez",
  "correo": "juan@email.com",
  "contrasena": "miPassword123"
}
```

### Reportes (`/reportes`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/reportes/crearReporte` | Crear nuevo reporte con geolocalización |
| `GET` | `/reportes/loadCategoria` | Obtener categorías de incidentes |
| `GET` | `/reportes/loadIncidentes/{id}` | Obtener incidentes por categoría |

#### Ejemplo: Crear reporte

```json
POST /reportes/crearReporte
{
  "geojson": {
    "type": "Feature",
    "properties": {
      "descripcion": "Bache en la calle principal"
    },
    "geometry": {
      "type": "Point",
      "coordinates": [-79.5341, 8.9824]
    }
  },
  "id_incidente": 1
}
```

### Capas Geográficas (`/capas`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/capas/provincias` | Obtener GeoJSON de provincias |
| `GET` | `/capas/distritos` | Obtener GeoJSON de distritos |
| `GET` | `/capas/corregimientos` | Obtener GeoJSON de corregimientos |
| `GET` | `/capas/reportes` | Obtener GeoJSON de reportes |

## 📁 Estructura del Proyecto

```
APISystemReport/
├── 📄 requirements.txt      # Dependencias del proyecto
├── 📄 README.md             # Documentación
└── 📁 app/
    ├── 📄 __init__.py
    ├── 📄 main.py           # Punto de entrada de la aplicación
    ├── 📁 DataBase/
    │   ├── 📄 __init__.py
    │   └── 📄 db.py         # Configuración de conexión a BD
    ├── 📁 Models/
    │   ├── 📄 __init__.py
    │   ├── 📄 ReportesModel.py   # Modelos Pydantic para reportes
    │   └── 📄 usuariosModel.py   # Modelos Pydantic para usuarios
    └── 📁 routers/
        ├── 📄 __init__.py
        ├── 📄 capas.py      # Endpoints de capas geográficas
        ├── 📄 reportes.py   # Endpoints de reportes
        └── 📄 usuarios.py   # Endpoints de usuarios
```

## Base de Datos

La API requiere las siguientes funciones y procedimientos en PostgreSQL:

### Funciones requeridas:
- `registrar_usuario(nombre, apellido, correo, contrasena)` - Registra usuarios
- `autenticar_usuario(email, password)` - Autentica usuarios
- `get_categorias()` - Retorna categorías de incidentes
- `get_incidentes_por_categoria(id)` - Retorna incidentes por categoría

### Procedimientos requeridos:
- `insertar_reportes(geometry, properties, id_incidente)` - Inserta reportes

### Vistas requeridas:
- `v_provincias_geojson` - GeoJSON de provincias
- `vista_distritos` - GeoJSON de distritos
- `vista_por_corregimientos_geojson` - GeoJSON de corregimientos
- `vista_reportes_geojson` - GeoJSON de reportes

---

<div align="center">

Desarrollado usando [FastAPI](https://fastapi.tiangolo.com/)

</div>
