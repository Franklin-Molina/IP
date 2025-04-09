from typing import Dict
from pydantic_ai import RunContext, ModelRetry
import logfire


async def obtener_gitignore_python(ctx: RunContext, dummy: str = "") -> str:
    """
    Devuelve una plantilla estándar para un archivo `.gitignore` usado en proyectos Python.

    Args:
        ctx: Contexto de ejecución del agente.
        dummy: Argumento sin usar, solo para compatibilidad, puede omitirse.

    Returns:
        Contenido en texto plano del archivo `.gitignore`.
    
    Si en el futuro fuera necesario, esta función puede mejorarse para obtener el template desde GitHub o fuentes oficiales.
    """
    try:
        plantilla = """
# Entornos virtuales
venv/
env/
ENV/
.venv/

# Archivos compilados de Python
__pycache__/
*.py[cod]
*$py.class

# Distribuciones y empaquetado
build/
dist/
*.egg-info/

# Configuración del entorno y archivos ocultos
*.env
.env.*
.env

# Notebooks de Jupyter y checkpoints
.ipynb_checkpoints/

# Archivos del sistema
.DS_Store
Thumbs.db
"""
        return plantilla.strip()
    except Exception as e:
        logfire.error(f"Error obteniendo .gitignore: {e}")
        raise ModelRetry("Error al obtener la plantilla .gitignore. Intenta nuevamente.")
