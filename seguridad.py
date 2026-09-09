import os
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

# Cargar variables del entorno desde el archivo .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "clave_de_prueba_super_secreta_123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Configuración de encriptación bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración para que Swagger UI sepa dónde pedir el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# 1. ENCRIPTAR CONTRASEÑA (Para no guardarla en texto plano)
def encriptar_password(password: str) -> str:
    return pwd_context.hash(password)


# 2. VERIFICAR CONTRASEÑA (Compara texto plano contra el hash guardado)
def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 3. CREAR TOKEN JWT (Genera la credencial digital con tiempo de expiración)
def crear_access_token(data: dict) -> str:
    to_encode = data.copy()
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiracion})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 4. OBTENER USUARIO ACTUAL (Lee el token enviando ERROR 401 si es falso o vencido)
def obtener_usuario_actual(token: str = Depends(oauth2_scheme)) -> dict:
    excepcion_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        rol: str = payload.get("rol")
        if username is None or rol is None:
            raise excepcion_401
        return {"username": username, "rol": rol}
    except jwt.PyJWTError:
        raise excepcion_401


# 5. EXIGIR ROL ADMINISTRADOR (Lee el usuario del token y envía ERROR 403 si no es admin)
def requerir_admin(usuario_actual: dict = Depends(obtener_usuario_actual)) -> dict:
    if usuario_actual.get("rol") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: Se requieren privilegios de Administrador"
        )
    return usuario_actual