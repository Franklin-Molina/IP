from flask import Flask
from app.core.database import engine, Base
from app.models import url, visit  # Importar los modelos

def create_app():
    """
    Función para crear y configurar la aplicación Flask.
    """
    app = Flask(__name__)

    # Crear las tablas de la base de datos
    Base.metadata.create_all(bind=engine)

    return app
