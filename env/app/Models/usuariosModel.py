from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    nombre:str
    apellido:str
    correo:str
    contrasena:str

class UsuarioRegistrado(BaseModel):
    email:str
    password:str

    