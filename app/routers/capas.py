from fastapi import APIRouter, HTTPException, Request
import asyncpg
from asyncpg import Connection
from typing import Optional
import json

router = APIRouter(
    prefix="/capas",
    tags=["capas"]

)
VISTAS = {
    "provincias": "v_provincias_geojson",
    "distritos": "vista_distritos",
    "corregimientos": "vista_por_corregimientos_geojson",
    "reportes": "vista_reportes_geojson",
}


@router.get("/{capa}")
async def get_mapa(capa: str, request: Request):
    
    if capa not in VISTAS:
        raise HTTPException(status_code= 404,detail= f"Capa Inválida. Opciones {list(VISTAS.keys())}")
    try:
        db_pool = request.app.state.db_pool
        async with db_pool.acquire() as conn:
            query = f"SELECT geojson FROM {VISTAS[capa]}"
            result = await conn.fetchrow(query)

            return json.loads(result["geojson"])if result else None
            
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code= 500, detail= f"Error al cargar capa: {str(e)}")


