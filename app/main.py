from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import capas, reportes,usuarios
from app.DataBase.db import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await init_db()
    yield
    await app.state.db_pool.close()


app = FastAPI(
    title="API Geoespacial",
    version="1.0",
    lifespan=lifespan
)


# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajustar en producción
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir routers
app.include_router(capas.router)
app.include_router(reportes.router)
app.include_router(usuarios.router)

