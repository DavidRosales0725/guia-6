import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Importar las rutas de la carpeta routers
from routers import usuarios, rutinas

app = FastAPI(
    title="FitTrack API",
    description="API REST para la gestión de usuarios, rutinas y progreso físico",
    version="1.0.0"
)

# Configuración de CORS (permite que cualquier navegador o frontend consulte la API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(usuarios.router)
app.include_router(rutinas.router)

# Endpoint de salud (Health Check obligatorio para la guía)
@app.get("/health", tags=["Salud"])
def health_check():
    return {"estado": "ok", "mensaje": "El servicio está corriendo correctamente"}

@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "Bienvenido a FitTrack API"}