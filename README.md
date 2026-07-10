<div align="center">

# 🌎 API System Report

**API REST geoespacial para reporte ciudadano de incidentes**, desarrollada con FastAPI y soporte nativo para datos GeoJSON. Diseñada para sistemas de monitoreo territorial donde ciudadanos o instituciones reportan incidentes georreferenciados (baches, fallas de infraestructura, etc.) organizados por provincia, distrito y corregimiento.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-PostGIS-336791?style=flat-square&logo=postgresql&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.11.4-E92063?style=flat-square&logo=pydantic&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.34.2-2E3440?style=flat-square)
![License](https://img.shields.io/badge/License-Private-lightgrey?style=flat-square)

</div>

---

## 💡 El problema que resuelve

Reportar incidentes urbanos (baches, daños en infraestructura, fallas de servicios) suele quedar disperso entre llamadas, redes sociales o quejas informales, sin ubicación exacta ni forma de agregarlos por zona geográfica. Esta API centraliza esos reportes con **coordenadas GeoJSON precisas**, permitiendo consultarlos y agruparlos por **provincia, distrito o corregimiento** — la base para cualquier dashboard de monitoreo territorial o sistema de atención ciudadana.

---

## 📑 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#️-configuración)
- [Uso](#-uso)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Base de Datos](#-base-de-datos)
- [Estructura del Proyecto](#-estructura-del-proyecto)

---

## ✨ Características

| | |
|---|---|
| 🔐 **Autenticación de usuarios** | Registro e inicio de sesión |
| 🗺️ **Soporte GeoJSON** | Manejo de datos geoespaciales con validación de geometrías |
| 📍 **Gestión de reportes** | Crear y categorizar reportes de incidentes |
| 🏙️ **Capas geográficas** | Consulta de provincias, distritos, corregimientos y reportes |
| ⚡ **Alto rendimiento** | Pool de conexiones asíncronas con asyncpg |
| 🌐 **CORS habilitado** | Listo para integrarse con frontends |

---

## 🛠️ Tecnologías

| Tecnología | Versión | Descripción |
|------------|---------|-------------|
| [FastAPI](https://fastapi.tiangolo.com/) | `0.115.12` | Framework web moderno y de alto rendimiento |
| [Uvicorn](https://www.uvicorn.org/) | `0.34.2` | Servidor ASGI para producción |
| [Gunicorn](https://gunicorn.org/) | — | Servidor WSGI para despliegue |
| [asyncpg](https://github.com/MagicStack/asyncpg) | `0.30.0` | Driver PostgreSQL asíncrono |
| [Pydantic](https://docs.pydantic.dev/) | `2.11.4` | Validación de datos |
| [geojson-pydantic](https://github.com/developmentseed/geojson-pydantic) | `2.0.0` | Modelos GeoJSON |

---

## 📋 Requisitos Previos

- Python 3.10+
- PostgreSQL con extensión PostGIS
- pip o pipenv

---

## 📦 Instalación

**1. Clonar el repositorio**

```bash
git clone https://github.com/erickAlejandr0/APISystemReport.git
cd APISystemReport
```

**2. Crear entorno virtual**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows
```

**3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuración

La aplicación utiliza variables de entorno para la configuración de la base de datos.

### Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `PG_USER` | Usuario de PostgreSQL | `postgres` |
| `PG_PASS` | Contraseña de PostgreSQL | `1234` |
| `PG_DB` | Nombre de la base de datos | `Panama` |
| `PG_HOST` | Host de la base de datos | `localhost` |
| `PG_PORT` | Puerto de PostgreSQL | `5432` |

### Archivo `.env` (recomendado)

```env
PG_USER=tu_usuario
PG_PASS=tu_contraseña
PG_DB=nombre_base_datos
PG_HOST=localhost
PG_PORT=5432
```

> ⚠️ Nunca subas tu `.env` real al repositorio. Usa un `.env.example` como plantilla.

---

## 🚀 Uso

### Desarrollo

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Producción

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Documentación interactiva

| Interfaz | URL |
|----------|-----|
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |

---

## 🔌 Endpoints de la API

### 👤 Usuarios `/usuarios`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/usuarios/registrar` | Registrar nuevo usuario |
| `POST` | `/usuarios/autenticar` | Autenticar usuario existente |

<details>
<summary><b>Ejemplo: Registrar usuario</b></summary>

```json
POST /usuarios/registrar
{
  "nombre": "Juan",
  "apellido": "Pérez",
  "correo": "juan@email.com",
  "contrasena": "miPassword123"
}
```

</details>

### 📍 Reportes `/reportes`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/reportes/crearReporte` | Crear nuevo reporte con geolocalización |
| `GET` | `/reportes/loadCategoria` | Obtener categorías de incidentes |
| `GET` | `/reportes/loadIncidentes/{id}` | Obtener incidentes por categoría |

<details>
<summary><b>Ejemplo: Crear reporte</b></summary>

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

</details>

### 🗺️ Capas Geográficas `/capas`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/capas/provincias` | Obtener GeoJSON de provincias |
| `GET` | `/capas/distritos` | Obtener GeoJSON de distritos |
| `GET` | `/capas/corregimientos` | Obtener GeoJSON de corregimientos |
| `GET` | `/capas/reportes` | Obtener GeoJSON de reportes |

---

## 🗄️ Base de Datos

La API requiere las siguientes funciones, procedimientos y vistas en PostgreSQL:

**Funciones**
- `registrar_usuario(nombre, apellido, correo, contrasena)` — Registra usuarios
- `autenticar_usuario(email, password)` — Autentica usuarios
- `get_categorias()` — Retorna categorías de incidentes
- `get_incidentes_por_categoria(id)` — Retorna incidentes por categoría

**Procedimientos**
- `insertar_reportes(geometry, properties, id_incidente)` — Inserta reportes

**Vistas**
- `v_provincias_geojson` — GeoJSON de provincias
- `vista_distritos` — GeoJSON de distritos
- `vista_por_corregimientos_geojson` — GeoJSON de corregimientos
- `vista_reportes_geojson` — GeoJSON de reportes

---

## 📁 Estructura del Proyecto

```
APISystemReport/
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Documentación
└── app/
    ├── __init__.py
    ├── main.py                # Punto de entrada de la aplicación
    ├── DataBase/
    │   ├── __init__.py
    │   └── db.py               # Configuración de conexión a BD
    ├── Models/
    │   ├── __init__.py
    │   ├── ReportesModel.py     # Modelos Pydantic para reportes
    │   └── usuariosModel.py     # Modelos Pydantic para usuarios
    └── routers/
        ├── __init__.py
        ├── capas.py             # Endpoints de capas geográficas
        ├── reportes.py          # Endpoints de reportes
        └── usuarios.py          # Endpoints de usuarios
```
---

<div align="center">

**Desarrollado por**

[![GitHub](https://img.shields.io/badge/GitHub-erickAlejandr0-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/erickAlejandr0)

Construido con [FastAPI](https://fastapi.tiangolo.com/)

</div>
