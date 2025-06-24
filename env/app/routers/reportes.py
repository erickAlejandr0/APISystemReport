from fastapi import APIRouter, HTTPException, Request
from app.Models.ReportesModel import ReporteRequest
import json
import asyncpg


router = APIRouter(
    prefix ="/reportes",
    tags=["reportes"]
)

@router.post("/crearReporte")
async def insertarReporte(reporte:ReporteRequest,  request: Request):
    try:
        db_pool = request.app.state.db_pool
        async with db_pool.acquire() as conn:
            await conn.execute(
                "CALL insertar_reportes($1,$2,$3)",
                json.dumps(reporte.geojson.geometry.model_dump()),
                json.dumps(reporte.geojson.properties),
                reporte.id_incidente
            )
            return{"insercion": True}
           
     
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500,detail= f"Error al enviar el reporte:{str(e)} + {type(e).__name__}")

        
@router.get("/loadCategoria")
async def selector(request: Request):
    try:
        db_pool = request.app.state.db_pool
        async with db_pool.acquire() as conn:
            result = await conn.fetch("SELECT * FROM get_categorias()")
            return result
    except asyncpg.PostgresError as e:
        raise HTTPException(500,f"error al cargar las categorias:{str(e)}")

@router.get("/loadIncidentes/{id}")
async def selector_Incidentes(id: int, request : Request):
    try:
        db_pool=request.app.state.db_pool
        async with db_pool.acquire() as conn:
            result = await conn.fetch(
                "SELECT * FROM get_incidentes_por_categoria($1)",
                id
            )
            return result
    except asyncpg.PostgresError as e:
        raise HTTPException(500,f"Error al cargar los incidentes{str(e)}") 


    








