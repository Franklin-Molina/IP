import random
import string
import requests
import json
import os
from sqlalchemy.orm import Session
from app.models.url import URL
from app.models.visit import Visit
from urllib.parse import urlparse
from app.core.database import IPINFO_API_KEY

def generate_short_code(length: int = 6) -> str:
    """
    Genera un código corto aleatorio para la URL.

    Args:
        length (int): Longitud del código. Por defecto 6.

    Returns:
        str: Código corto generado.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def is_valid_url(url: str) -> bool:
    """
    Valida si una URL tiene un formato correcto.

    Args:
        url (str): URL a validar.

    Returns:
        bool: True si es válida, False si no.
    """
    parsed = urlparse(url)
    return all([parsed.scheme in ("http", "https"), parsed.netloc])


def create_short_url(db: Session, original_url: str) -> URL:
    """
    Crea una URL acortada y la guarda en la base de datos.

    Args:
        db (Session): Sesión de base de datos.
        original_url (str): URL original.

    Returns:
        URL: Objeto URL creado.
    """
    if not is_valid_url(original_url):
        raise ValueError("URL inválida")

    # Generar un código único
    short_code = generate_short_code()
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    db_url = URL(original_url=original_url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_url_by_code(db: Session, short_code: str) -> URL | None:
    """
    Obtiene una URL original a partir del código corto.

    Args:
        db (Session): Sesión de base de datos.
        short_code (str): Código corto.

    Returns:
        URL | None: Objeto URL o None si no existe.
    """
    return db.query(URL).filter(URL.short_code == short_code).first()


def register_visit(
    db: Session,
    url_id: int,
    ip_address: str,
    user_agent: str | None = None,
    referrer: str | None = None,
    network_info: str | None = None,
    cookies: str | None = None,
    extra_params: str | None = None,
    device_info: str | None = None,
) -> Visit:
    """
    Registra una visita a una URL acortada.

    Args:
        db (Session): Sesión de base de datos.
        url_id (int): ID de la URL visitada.
        ip_address (str): Dirección IP del visitante.
        user_agent (str | None): Agente de usuario.
        referrer (str | None): URL de referencia.
        network_info (str | None): Información de red (JSON o texto).
        cookies (str | None): Cookies (JSON o texto).
        extra_params (str | None): Parámetros adicionales (JSON o texto).
        device_info (str | None): Sistema operativo y navegador.

    Returns:
        Visit: Objeto visita creada.
    """
    latitude = None
    longitude = None
    isp = None

    if IPINFO_API_KEY:
        try:
            url = f"https://ipinfo.io/{ip_address}?token={IPINFO_API_KEY}"
            response = requests.get(url)
            data = response.json()
            loc = data.get("loc")
            if loc:
                latitude, longitude = loc.split(",")
            isp = data.get("org")
        except Exception as e:
            print(f"Error al obtener geolocalización: {e}")

    visit = Visit(
        url_id=url_id,
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer,
        network_info=network_info,
        cookies=cookies,
        extra_params=extra_params,
        device_info=device_info,
        latitude=latitude,
        longitude=longitude,
        isp=isp,
    )
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit
