import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import init_db

load_dotenv()

# Importar los 4 routers
from routers import usuarios, ejercicios, rutinas, progreso

app = FastAPI(
    title="FitTrack API",
    description="API REST para la gestión de usuarios, ejercicios, rutinas y progreso físico",
    version="1.0.0"
)

# Inicializar tablas al arrancar el servidor
@app.on_event("startup")
def startup_event():
    init_db()

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

@app.get("/health", tags=["Salud"])
def health_check():
    return {"estado": "ok", "mensaje": "El servicio está corriendo correctamente"}

@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "Bienvenido a FitTrack API"}