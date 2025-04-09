from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router as url_router
from app.api.auth import router as auth_router
from app.core.database import Base, engine
from app.core.middleware import RateLimitMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Acortador de URLs")

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Middleware
app.add_middleware(RateLimitMiddleware)

# Routers
app.include_router(url_router)
app.include_router(auth_router)
