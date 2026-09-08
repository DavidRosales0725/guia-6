from pydantic import BaseModel
from typing import Optional

# --- SCHEMAS DE USUARIOS ---
class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str
    rol: Optional[str] = "usuario"

# --- SCHEMAS DE EJERCICIOS ---
class EjercicioCreate(BaseModel):
    nombre: str
    grupo_muscular: str
    descripcion: Optional[str] = None

# --- SCHEMAS DE RUTINAS ---
class RutinaCreate(BaseModel):
    usuario_id: int
    nombre: str
    descripcion: Optional[str] = None

# --- SCHEMAS DE PROGRESO (REGISTRO PESO) ---
class ProgresoCreate(BaseModel):
    usuario_id: int
    peso: float