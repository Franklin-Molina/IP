from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.url import create_short_url, get_url_by_code, register_visit
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/")
def root():
    """
    Redirige a la interfaz principal.
    """
    return RedirectResponse(url="/static/index.html")


def infer_device_info(user_agent: str | None) -> str:
    """
    Inferir sistema operativo y navegador a partir del User-Agent.

    Args:
        user_agent (str | None): Cadena User-Agent.

    Returns:
        str: Descripción del dispositivo, ej. "Windows 10 - Chrome".
    """
    if not user_agent:
        return "Desconocido"

    ua = user_agent.lower()
    # Sistema operativo
    if "windows" in ua:
        os = "Windows"
    elif "mac os" in ua or "macintosh" in ua:
        os = "MacOS"
    elif "linux" in ua:
        os = "Linux"
    elif "android" in ua:
        os = "Android"
    elif "iphone" in ua or "ipad" in ua:
        os = "iOS"
    else:
        os = "Otro"

    # Navegador
    if "chrome" in ua and "safari" in ua:
        browser = "Chrome"
    elif "firefox" in ua:
        browser = "Firefox"
    elif "safari" in ua and "chrome" not in ua:
        browser = "Safari"
    elif "edge" in ua:
        browser = "Edge"
    elif "opera" in ua or "opr" in ua:
        browser = "Opera"
    else:
        browser = "Otro"

    return f"{os} - {browser}"

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

    device_info = infer_device_info(user_agent)

    register_visit(
        db,
        url_obj.id,
        ip_address,
        user_agent=user_agent,
        referrer=referrer,
        network_info=network_info,
        cookies=cookies_json,
        extra_params=params_json,
        device_info=device_info,
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
        {
            "ip_address": visit.ip_address,
            "timestamp": visit.timestamp.isoformat(),
            "user_agent": visit.user_agent,
            "referrer": visit.referrer,
            "network_info": visit.network_info,
            "cookies": visit.cookies,
            "extra_params": visit.extra_params,
            "device_info": visit.device_info,
            "latitude": visit.latitude,
            "longitude": visit.longitude,
            "isp": visit.isp,
        }
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


from fastapi import status

@router.delete("/api/urls/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_url(short_code: str, db: Session = Depends(get_db)):
    """
    Borra una URL acortada por su código.
    """
    url_obj = get_url_by_code(db, short_code)
    if not url_obj:
        raise HTTPException(status_code=404, detail="URL no encontrada")
    db.delete(url_obj)
    db.commit()


@router.delete("/api/urls", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_urls(db: Session = Depends(get_db)):
    """
    Borra todas las URLs acortadas.
    """
    from app.models.url import URL
    urls = db.query(URL).all()
    for url in urls:
        db.delete(url)
    db.commit()

@router.get("/debug/visit-columns")
def debug_visit_columns():
    """
    Devuelve las columnas actuales de la tabla visits para depuración.
    """
    from app.models.visit import Visit
    return [c.name for c in Visit.__table__.columns]
