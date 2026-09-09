import sqlite3
from fastapi import APIRouter, HTTPException, Depends
from schemas import UsuarioCreate
from database import get_db
from seguridad import encriptar_password, obtener_usuario_actual, requerir_admin

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

# 1. Listar todos los usuarios (Ruta Pública - Sin candado)
@router.get("/")
def obtener_usuarios():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, rol, fecha_registro FROM usuarios")
    usuarios = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return usuarios

# 2. Obtener un usuario por ID (Ruta Pública - Sin candado)
@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, rol, fecha_registro FROM usuarios WHERE id = ?", (usuario_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return dict(row)

# 3. Crear un nuevo usuario (Encripta la contraseña automáticamente)
@router.post("/", status_code=201)
def crear_usuario(usuario: UsuarioCreate):
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Encriptar contraseña antes de guardar en la BD
        password_hash = encriptar_password(usuario.password)
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password, rol) VALUES (?, ?, ?, ?)",
            (usuario.nombre, usuario.email, password_hash, usuario.rol)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        conn.close()
        return {"mensaje": "Usuario creado exitosamente", "id": nuevo_id}
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Error al crear usuario: {str(e)}")

# 4. Eliminar usuario (AQUÍ APARECE EL CANDADO Y RETORNA 403 SI NO ES ADMIN)
@router.delete("/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    admin_actual: dict = Depends(requerir_admin) # <--- MUESTRA EL CANDADO Y VALIDA ROL ADMIN
):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    conn.commit()
    filas = cursor.rowcount
    conn.close()
    if filas == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": f"Usuario {usuario_id} eliminado exitosamente por el administrador {admin_actual['username']}"}