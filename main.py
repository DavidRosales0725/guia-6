import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
from database import init_db, get_db as obtener_conexion

from database import init_db, obtener_conexion
from seguridad import (
    encriptar_password,
    verificar_password,
    crear_access_token,
    obtener_usuario_actual,
    requerir_admin
)

# Cargar variables de entorno
load_dotenv()

# Inicializar la base de datos y crear las tablas
init_db()

# Importar los 4 routers
from routers import usuarios, ejercicios, rutinas, progreso

app = FastAPI(
    title="FitTrack API",
    description="API REST para la gestión de usuarios, ejercicios, rutinas y progreso físico",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar los 4 routers (14 endpoints en total)
app.include_router(usuarios.router)
app.include_router(ejercicios.router)
app.include_router(rutinas.router)
app.include_router(progreso.router)

# Endpoint de Login (Genera el Token y habilita el botón Authorize en Swagger /docs)
@app.post("/login", tags=["Autenticación"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    # Busca coincidencia tanto en la columna email como en nombre
    cursor.execute(
        "SELECT * FROM usuarios WHERE email = ? OR nombre = ?", 
        (form_data.username, form_data.username)
    )
    usuario = cursor.fetchone()
    conn.close()
    
    # Validar credenciales
    if not usuario or not verificar_password(form_data.password, usuario["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generar token JWT usando el email o nombre como identidad (sub)
    access_token = crear_access_token(
        data={"sub": usuario["email"], "rol": usuario["rol"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/health", tags=["Salud"])
def health_check():
    return {"estado": "ok", "mensaje": "El servicio está corriendo correctamente"}

@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "Bienvenido a FitTrack API"}