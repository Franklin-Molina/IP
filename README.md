# Acortador de URLs

## Descripción

Sistema web para acortar URLs y capturar información de visitas.

## Configuración

1.  Crear un entorno virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate.bat  # Windows
    ```
2.  Instalar dependencias:

    ```bash
    pip install -r requirements.txt
    ```
3.  Configurar variables de entorno:

    -   Crear un archivo `.env` basado en `.env.example`.
    -   Establecer la variable `OPENAI_API_KEY` con tu clave de OpenAI.

## Ejecución

```bash
uvicorn main:app --reload
```

Acceder a:

-   Panel de administración: `http://localhost:8000/static/admin.html`
-   Interfaz principal: `http://localhost:8000/static/index.html`

## Pruebas

Acceder a:

-   `/api/stats/<short_code>` para ver estadísticas de una URL.
-   `/debug/visit-columns` para ver las columnas de la tabla `visits`.
