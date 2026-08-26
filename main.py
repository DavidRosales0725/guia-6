from fastapi import FastAPI, HTTPException, status
from typing import List
import database
import schemas

app = FastAPI(
    title="FitTrack API",
    description="API REST completa para la gestión de entrenamiento y progreso físico",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    database.init_db()

@app.get("/", tags=["Inicio"])
def index():
    return {"mensaje": "¡Bienvenido a la API de FitTrack!"}

# ==========================================
# 1. USUARIOS (CRUD COMPLETO)
# ==========================================
@app.post("/usuarios", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def crear_usuario(usuario: schemas.UsuarioCreate):
    conn = database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES (?, ?, ?, ?)",
            (usuario.nombre, usuario.email, usuario.password, usuario.rol)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        return {**usuario.model_dump(), "id": nuevo_id}
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="El correo ya se encuentra registrado")
    finally:
        conn.close()

@app.get("/usuarios", response_model=List[schemas.UsuarioResponse], tags=["Usuarios"])
def listar_usuarios():
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, rol, fecha_registro FROM usuarios")
    usuarios = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return usuarios

@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse, tags=["Usuarios"])
def obtener_usuario(usuario_id: int):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, rol, fecha_registro FROM usuarios WHERE id = ?", (usuario_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return dict(row)

@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse, tags=["Usuarios"])
def actualizar_usuario(usuario_id: int, datos: schemas.UsuarioUpdate):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, rol, fecha_registro FROM usuarios WHERE id = ?", (usuario_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    nuevo_nombre = datos.nombre if datos.nombre is not None else user["nombre"]
    nuevo_email = datos.email if datos.email is not None else user["email"]
    nuevo_rol = datos.rol if datos.rol is not None else user["rol"]

    cursor.execute(
        "UPDATE usuarios SET nombre = ?, email = ?, rol = ? WHERE id = ?",
        (nuevo_nombre, nuevo_email, nuevo_rol, usuario_id)
    )
    conn.commit()
    conn.close()
    return {"id": usuario_id, "nombre": nuevo_nombre, "email": nuevo_email, "rol": nuevo_rol, "fecha_registro": user["fecha_registro"]}

@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Usuarios"])
def eliminar_usuario(usuario_id: int):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    conn.commit()
    conn.close()
    return None

# ==========================================
# 2. EJERCICIOS (CRUD COMPLETO)
# ==========================================
@app.post("/ejercicios", response_model=schemas.EjercicioResponse, status_code=status.HTTP_201_CREATED, tags=["Ejercicios"])
def crear_ejercicio(ejercicio: schemas.EjercicioCreate):
    conn = database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO ejercicios (nombre, grupo_muscular, descripcion) VALUES (?, ?, ?)",
            (ejercicio.nombre, ejercicio.grupo_muscular, ejercicio.descripcion)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        return {**ejercicio.model_dump(), "id": nuevo_id}
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Ese ejercicio ya existe")
    finally:
        conn.close()

@app.get("/ejercicios", response_model=List[schemas.EjercicioResponse], tags=["Ejercicios"])
def listar_ejercicios():
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, grupo_muscular, descripcion FROM ejercicios")
    ejercicios = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return ejercicios

@app.put("/ejercicios/{ejercicio_id}", response_model=schemas.EjercicioResponse, tags=["Ejercicios"])
def actualizar_ejercicio(ejercicio_id: int, datos: schemas.EjercicioUpdate):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ejercicios WHERE id = ?", (ejercicio_id,))
    ejercicio = cursor.fetchone()
    if not ejercicio:
        conn.close()
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    n_nombre = datos.nombre if datos.nombre is not None else ejercicio["nombre"]
    n_grupo = datos.grupo_muscular if datos.grupo_muscular is not None else ejercicio["grupo_muscular"]
    n_desc = datos.descripcion if datos.descripcion is not None else ejercicio["descripcion"]

    cursor.execute(
        "UPDATE ejercicios SET nombre = ?, grupo_muscular = ?, descripcion = ? WHERE id = ?",
        (n_nombre, n_grupo, n_desc, ejercicio_id)
    )
    conn.commit()
    conn.close()
    return {"id": ejercicio_id, "nombre": n_nombre, "grupo_muscular": n_grupo, "descripcion": n_desc}

@app.delete("/ejercicios/{ejercicio_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Ejercicios"])
def eliminar_ejercicio(ejercicio_id: int):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ejercicios WHERE id = ?", (ejercicio_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    conn.commit()
    conn.close()
    return None

# ==========================================
# 3. RUTINAS (CRUD COMPLETO)
# ==========================================
@app.post("/rutinas", response_model=schemas.RutinaResponse, status_code=status.HTTP_201_CREATED, tags=["Rutinas"])
def crear_rutina(rutina: schemas.RutinaCreate):
    conn = database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO rutinas (usuario_id, nombre, descripcion) VALUES (?, ?, ?)",
            (rutina.usuario_id, rutina.nombre, rutina.descripcion)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        return {**rutina.model_dump(), "id": nuevo_id}
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Error al crear rutina. Verifica el usuario_id.")
    finally:
        conn.close()

@app.get("/rutinas", response_model=List[schemas.RutinaResponse], tags=["Rutinas"])
def listar_rutinas():
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario_id, nombre, descripcion, fecha_creacion FROM rutinas")
    rutinas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rutinas

@app.delete("/rutinas/{rutina_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Rutinas"])
def eliminar_rutina(rutina_id: int):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rutinas WHERE id = ?", (rutina_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    conn.commit()
    conn.close()
    return None

# ==========================================
# 4. REGISTRO DE PESO / PROGRESO
# ==========================================
@app.post("/peso", response_model=schemas.RegistroPesoResponse, status_code=status.HTTP_201_CREATED, tags=["Progreso"])
def registrar_peso(registro: schemas.RegistroPesoCreate):
    conn = database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO registro_peso (usuario_id, peso) VALUES (?, ?)",
            (registro.usuario_id, registro.peso)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid
        return {**registro.model_dump(), "id": nuevo_id}
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Error al registrar peso. Verifica el usuario_id.")
    finally:
        conn.close()

@app.get("/peso/{usuario_id}", response_model=List[schemas.RegistroPesoResponse], tags=["Progreso"])
def historial_peso(usuario_id: int):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario_id, peso, fecha FROM registro_peso WHERE usuario_id = ?", (usuario_id,))
    registros = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return registros

@app.delete("/peso/{registro_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Progreso"])
def eliminar_registro_peso(registro_id: int):
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM registro_peso WHERE id = ?", (registro_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Registro de peso no encontrado")
    conn.commit()
    conn.close()
    return None