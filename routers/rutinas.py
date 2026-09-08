from fastapi import APIRouter, HTTPException
import sqlite3
from schemas import RutinaCreate
from database import get_db

router = APIRouter(
    prefix="/rutinas",
    tags=["Rutinas"]
)

@router.get("/")
def obtener_rutinas():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rutinas")
    rutinas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rutinas

@router.get("/{rutina_id}")
def obtener_rutina(rutina_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rutinas WHERE id = ?", (rutina_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    return dict(row)

@router.post("/", status_code=201)
def crear_rutina(rutina: RutinaCreate):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (rutina.usuario_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="El usuario asignado a la rutina no existe")

    cursor.execute(
        "INSERT INTO rutinas (usuario_id, nombre, descripcion) VALUES (?, ?, ?)",
        (rutina.usuario_id, rutina.nombre, rutina.descripcion)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return {"mensaje": "Rutina creada exitosamente", "id": nuevo_id}