from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from app.api.routes import router as url_router
from app.api.auth import router as auth_router
from app.core.database import Base, engine
from app.core.middleware import RateLimitMiddleware

# Configuración de la base de datos
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./app.db")  # SQLite por defecto
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Acortador de URLs", debug=os.environ.get("DEBUG", "False") == "True")

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Middleware
app.add_middleware(RateLimitMiddleware)

# Routers
app.include_router(url_router)
app.include_router(auth_router)
