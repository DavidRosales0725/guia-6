from pydantic import BaseModel
from typing import Optional

# --- 1. USUARIOS ---
class UsuarioBase(BaseModel):
    nombre: str
    email: str
    rol: Optional[str] = "usuario"

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    rol: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int
    fecha_registro: Optional[str] = None

# --- 2. EJERCICIOS ---
class EjercicioBase(BaseModel):
    nombre: str
    grupo_muscular: str
    descripcion: Optional[str] = None

class EjercicioCreate(EjercicioBase):
    pass

class EjercicioUpdate(BaseModel):
    nombre: Optional[str] = None
    grupo_muscular: Optional[str] = None
    descripcion: Optional[str] = None

class EjercicioResponse(EjercicioBase):
    id: int

# --- 3. RUTINAS ---
class RutinaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RutinaCreate(RutinaBase):
    usuario_id: int

class RutinaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class RutinaResponse(RutinaBase):
    id: int
    usuario_id: int
    fecha_creacion: Optional[str] = None

# --- 4. REGISTRO DE PESO ---
class RegistroPesoCreate(BaseModel):
    usuario_id: int
    peso: float

class RegistroPesoResponse(RegistroPesoCreate):
    id: int
    fecha: Optional[str] = None