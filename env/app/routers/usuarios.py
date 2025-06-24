from fastapi import APIRouter, HTTPException,Request
from app.Models.usuariosModel import Usuario,UsuarioRegistrado
import asyncpg

router = APIRouter(
    prefix ="/usuarios",
    tags=["usuarios"]
)
@router.post("/registrar")
async def registrar_usuario(usuario: Usuario,  request: Request):
    try:
        db_pool = request.app.state.db_pool
        async with db_pool.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT registrar_usuario($1,$2,$3,$4) AS value",
                    usuario.nombre,
                    usuario.apellido,
                    usuario.correo,
                    usuario.contrasena  
            )
            if result:
                return{"registro":True,
                       "id_usuario": result['value']
                }
            raise HTTPException(500, "Error al registrar el usuario")
        
    except Exception as e:
        raise HTTPException(500, f"Error inesperado: {str(e)}")
    except asyncpg.UniqueViolationError as e:
        raise HTTPException(400, f"El correo ya está registrado {str(e)}")
    except asyncpg.UndefinedFunctionError as e:
        raise HTTPException(500, f"La función no existe o los parámetros son incorrectos {str(e)}")
    except asyncpg.PostgresError as e:
        raise HTTPException(500, f"Error de base de datos: {str(e)}")
   
   
    
@router.post("/autenticar")
async def autenticar_usuario(usuario: UsuarioRegistrado, request : Request):
    try:
        db_pool = request.app.state.db_pool
        async with db_pool.acquire() as conn:
            result = await conn.fetchrow(
                "SELECT * FROM autenticar_usuario($1,$2)",
                    usuario.email,
                    usuario.password
            )
            if result:
                return(result)
            raise HTTPException(500,"error al autenticar")
    except Exception as e:
        raise HTTPException(500,f"Error al autenticar{str(e)}")
    except asyncpg.PostgresError as e:
        raise HTTPException(500, f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(500, f"Error inesperado: {str(e)}")

