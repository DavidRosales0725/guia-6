from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter(
    prefix="/rutinas",
    tags=["Rutinas"]
)

DB_NAME = "fittrack.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/")
def obtener_rutinas():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rutinas")
    rutinas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rutinas