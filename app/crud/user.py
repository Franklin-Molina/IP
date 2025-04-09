from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Obtiene un usuario por su nombre de usuario.

    Args:
        db (Session): Sesión de base de datos.
        username (str): Nombre de usuario.

    Returns:
        User | None: Usuario o None si no existe.
    """
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str) -> User:
    """
    Crea un nuevo usuario con contraseña hasheada.

    Args:
        db (Session): Sesión de base de datos.
        username (str): Nombre de usuario.
        password (str): Contraseña en texto plano.

    Returns:
        User: Usuario creado.
    """
    hashed_password = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña coincide con el hash.

    Args:
        plain_password (str): Contraseña en texto plano.
        hashed_password (str): Hash almacenado.

    Returns:
        bool: True si coincide, False si no.
    """
    return pwd_context.verify(plain_password, hashed_password)
