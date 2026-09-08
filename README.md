# 🏋️‍♂️ FitTrack API - Backend (Guía 6 SENA)

API RESTful desarrollada con **FastAPI**, **SQLite3** y **Pydantic** para la gestión e historial de entrenamientos y progreso físico.

Este proyecto corresponde a la evidencia de desarrollo de la **Guía de Aprendizaje 6** del programa **Análisis y Desarrollo de Software (ADSO) - SENA**.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Framework Web:** FastAPI
* **Servidor ASGI:** Uvicorn
* **Base de Datos:** SQLite3 (Motor relacional nativo)
* **Validación de Datos:** Pydantic
* **Documentación:** Swagger UI / OpenAPI (Autogenerada)

---

## 📋 Entidades del Sistema

El sistema gestiona 4 entidades relacionales principales:

1. **Usuarios (`/usuarios`):** Gestión de cuentas, roles (`administrador` / `usuario`) y fechas de registro.
2. **Ejercicios (`/ejercicios`):** Catálogo de ejercicios clasificados por grupo muscular.
3. **Rutinas (`/rutinas`):** Planificación de rutinas asociadas a un usuario.
4. **Progreso (`/peso`):** Historial de registro de peso corporal por usuario.

---

## 🚀 Instalación y Configuración Local

Sigue estos pasos para clonar y ejecutar la API en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/fittrack-backend.git](https://github.com/TU_USUARIO/fittrack-backend.git)
cd fittrack-backend
```

### 2. Crear y activar el entorno virtual

* **En Windows (Git Bash):**
  ```bash
  python -m venv venv
  source venv/Scripts/activate
  ```

### 3. Instalar dependencias
```bash
pip install fastapi uvicorn pydantic
```

### 4. Inicializar la Base de Datos
```bash
python database.py
```

### 5. Iniciar el servidor de desarrollo
```bash
python -m uvicorn main:app --reload
```

El servidor quedará corriendo en: `http://127.0.0.1:8000`

---

## 📖 Documentación Interactiva (Swagger UI)

Una vez iniciado el servidor, puedes probar todas las operaciones CRUD desde el navegador ingresando a:

👉 **`http://127.0.0.1:8000/docs`**

---

## 📌 Endpoints Principales

| Módulo | Método | Endpoint | Descripción |
| :--- | :--- | :--- | :--- |
| **Usuarios** | `POST` | `/usuarios` | Registrar nuevo usuario |
| | `GET` | `/usuarios` | Listar todos los usuarios |
| | `PUT` | `/usuarios/{id}` | Actualizar usuario por ID |
| | `DELETE` | `/usuarios/{id}` | Eliminar usuario por ID |
| **Ejercicios** | `POST` | `/ejercicios` | Crear ejercicio |
| | `GET` | `/ejercicios` | Listar ejercicios |
| | `DELETE` | `/ejercicios/{id}` | Eliminar ejercicio por ID |
| **Rutinas** | `POST` | `/rutinas` | Crear rutina asociada a usuario |
| | `GET` | `/rutinas` | Listar rutinas registradas |
| **Progreso** | `POST` | `/peso` | Registrar peso de usuario |
| | `GET` | `/peso/{usuario_id}` | Ver historial de peso por usuario |

---

## Despliegue en Producción

- **URL Pública:** https://fittrack-api-kxn2.onrender.com
- **Documentación Swagger:** https://fittrack-api-kxn2.onrender.com/docs
- **Endpoint de Salud:** https://fittrack-api-kxn2.onrender.com/health

### Limitaciones Conocidas (Plan Gratuito de Render)
- **Sistema de archivos efímero:** La base de datos SQLite se reinicia y borra en cada redespliegue o reinicio del contenedor.
- **Inactividad (Spin down):** Tras 15 minutos sin recibir peticiones, el servidor se suspende automáticamente. La primera petición puede tardar cerca de 50 segundos en responder mientras la instancia se vuelve a levantar.

## 👤 Autor

* **David Alejandro Rosales Sarria**
* **Programa:** Análisis y Desarrollo de Software (ADSO) - SENA