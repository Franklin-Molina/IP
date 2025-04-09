from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.url import create_short_url, get_url_by_code, register_visit
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

router = APIRouter()

class URLRequest(BaseModel):
    url: str

@router.post("/api/shorten")
def shorten_url(request_data: URLRequest, db: Session = Depends(get_db)):
    """
    Crea una URL acortada a partir de una URL original.
    """
    try:
        url_obj = create_short_url(db, request_data.url)
    except ValueError:
        raise HTTPException(status_code=400, detail="URL inválida")
    return {"short_code": url_obj.short_code, "original_url": url_obj.original_url}


@router.get("/{short_code}")
def redirect_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    """
    Redirige a la URL original y registra la visita.
    """
    url_obj = get_url_by_code(db, short_code)
    if not url_obj:
        raise HTTPException(status_code=404, detail="URL no encontrada")

    ip_address = request.client.host

    # Extraer cabeceras
    user_agent = request.headers.get("user-agent")
    referrer = request.headers.get("referer")

    # Extraer cookies (como dict serializado a string)
    cookies_dict = dict(request.cookies)
    import json
    cookies_json = json.dumps(cookies_dict, ensure_ascii=False)

    # Extraer query params (como dict serializado a string)
    params_dict = dict(request.query_params)
    params_json = json.dumps(params_dict, ensure_ascii=False)

    # Inferir info de red (placeholder)
    network_info = json.dumps({
        "connection_type": "desconocido",
        "proxy": request.headers.get("via") or "no detectado",
        "vpn": "desconocido"
    }, ensure_ascii=False)

    register_visit(
        db,
        url_obj.id,
        ip_address,
        user_agent=user_agent,
        referrer=referrer,
        network_info=network_info,
        cookies=cookies_json,
        extra_params=params_json,
    )

    return RedirectResponse(url=url_obj.original_url)


@router.get("/api/stats/{short_code}")
def url_stats(short_code: str, db: Session = Depends(get_db)):
    """
    Devuelve estadísticas de visitas para una URL acortada.
    """
    url_obj = get_url_by_code(db, short_code)
    if not url_obj:
        raise HTTPException(status_code=404, detail="URL no encontrada")

    visits = [
        {"ip_address": visit.ip_address, "timestamp": visit.timestamp.isoformat()}
        for visit in url_obj.visits
    ]
    return {
        "original_url": url_obj.original_url,
        "short_code": url_obj.short_code,
        "visits": visits,
        "total_visits": len(visits),
    }

@router.get("/api/user/urls")
def get_user_urls(db: Session = Depends(get_db)):
    """
    Devuelve todas las URLs acortadas (simulación de URLs del usuario).
    """
    from app.models.url import URL  # Importación local para evitar ciclos
    urls = db.query(URL).all()
    result = []
    for url in urls:
        result.append({
            "short_code": url.short_code,
            "original_url": url.original_url,
            "total_visits": len(url.visits)
        })
    return result


@router.get("/debug/visit-columns")
def debug_visit_columns():
    """
    Devuelve las columnas actuales de la tabla visits para depuración.
    """
    from app.models.visit import Visit
    return [c.name for c in Visit.__table__.columns]
