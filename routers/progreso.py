from fastapi import APIRouter, HTTPException
import sqlite3
from schemas import ProgresoCreate

router = APIRouter(
    prefix="/progreso",
    tags=["Progreso"]
)

DB_NAME = "fittrack.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# 1. Listar todo el registro de peso
@router.get("/")
def obtener_registros():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registro_peso")
    registros = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return registros

# 2. Obtener un registro por ID
@router.get("/{registro_id}")
def obtener_registro(registro_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registro_peso WHERE id = ?", (registro_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Registro de progreso no encontrado")
    return dict(row)

# 3. Crear un nuevo registro de peso
@router.post("/", status_code=201)
def crear_registro(progreso: ProgresoCreate):
    conn = get_db()
    cursor = conn.cursor()
    
    # Verificar si el usuario existe
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (progreso.usuario_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="El usuario asignado no existe")

    cursor.execute(
        "INSERT INTO registro_peso (usuario_id, peso) VALUES (?, ?)",
        (progreso.usuario_id, progreso.peso)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return {"mensaje": "Registro de peso guardado exitosamente", "id": nuevo_id}