from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

DB_NAME = "fittrack.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/")
def obtener_usuarios():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, fecha_registro FROM usuarios")
    usuarios = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return usuarios