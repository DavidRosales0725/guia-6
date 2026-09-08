from fastapi import APIRouter, HTTPException
import sqlite3
from schemas import EjercicioCreate

router = APIRouter(
    prefix="/ejercicios",
    tags=["Ejercicios"]
)

DB_NAME = "fittrack.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# 1. Listar todos los ejercicios
@router.get("/")
def obtener_ejercicios():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ejercicios")
    ejercicios = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return ejercicios

# 2. Obtener un ejercicio por ID
@router.get("/{ejercicio_id}")
def obtener_ejercicio(ejercicio_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ejercicios WHERE id = ?", (ejercicio_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return dict(row)

# 3. Crear un nuevo ejercicio
@router.post("/", status_code=201)
def crear_ejercicio(ejercicio: EjercicioCreate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ejercicios (nombre, grupo_muscular, descripcion) VALUES (?, ?, ?)",
        (ejercicio.nombre, ejercicio.grupo_muscular, ejercicio.descripcion)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return {"mensaje": "Ejercicio creado exitosamente", "id": nuevo_id}

# 4. Eliminar un ejercicio
@router.delete("/{ejercicio_id}")
def eliminar_ejercicio(ejercicio_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ejercicios WHERE id = ?", (ejercicio_id,))
    conn.commit()
    filas = cursor.rowcount
    conn.close()
    if filas == 0:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return {"mensaje": "Ejercicio eliminado exitosamente"}