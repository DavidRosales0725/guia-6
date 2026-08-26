import sqlite3

DATABASE_NAME = "fittrack.db"

def get_connection():
    """Establece conexión con la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea las 4 tablas principales de FitTrack."""
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Tabla Usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        rol TEXT CHECK(rol IN ('administrador', 'usuario')) DEFAULT 'usuario',
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Tabla Ejercicios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ejercicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        grupo_muscular TEXT NOT NULL,
        descripcion TEXT
    );
    """)

    # 3. Tabla Rutinas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rutinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
    );
    """)

    # 4. Tabla Registro de Peso (Progreso)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registro_peso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        peso REAL NOT NULL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print("¡Base de datos con 4 entidades creada exitosamente!")

if __name__ == "__main__":
    init_db()