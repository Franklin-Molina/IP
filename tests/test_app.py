import pytest
from fastapi.testclient import TestClient
from app.crud.url import generate_short_code, is_valid_url
from main import app

client = TestClient(app)

def test_generate_short_code_length():
    """Caso esperado: código de longitud correcta"""
    code = generate_short_code(8)
    assert len(code) == 8

def test_generate_short_code_uniqueness():
    """Caso periférico: alta probabilidad de unicidad"""
    codes = {generate_short_code() for _ in range(1000)}
    assert len(codes) == 1000

def test_generate_short_code_invalid_length():
    """Caso fallo: longitud negativa"""
    with pytest.raises(ValueError):
        generate_short_code(-1)

def test_shorten_url_success():
    """Caso esperado: acortar URL válida"""
    response = client.post("/api/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data
    assert "original_url" in data

def test_shorten_url_invalid():
    """Caso fallo: URL inválida"""
    response = client.post("/api/shorten", json={"url": "notaurl"})
    assert response.status_code == 400

def test_redirect_and_stats():
    """Caso esperado: redirigir y obtener stats"""
    # Crear URL
    response = client.post("/api/shorten", json={"url": "https://example.com"})
    data = response.json()
    code = data["short_code"]

    # Redirigir
    redirect = client.get(f"/{code}", allow_redirects=False)
    assert redirect.status_code == 307 or redirect.status_code == 302

    # Stats
    stats = client.get(f"/api/stats/{code}")
    assert stats.status_code == 200
    stats_data = stats.json()
    assert stats_data["total_visits"] >= 1
    assert "visits" in stats_data


def test_redirect_with_headers_cookies_params():
    """Caso esperado: registrar visita con headers, cookies y query params personalizados"""
    # Crear URL
    response = client.post("/api/shorten", json={"url": "https://example.com"})
    data = response.json()
    code = data["short_code"]

    headers = {
        "User-Agent": "TestAgent/1.0",
        "Referer": "https://referrer.com",
        "Via": "proxy.example.com"
    }
    cookies = {"sessionid": "abc123", "userid": "user42"}
    params = {"utm_source": "newsletter", "campaign": "spring"}

    # Redirigir con datos personalizados
    redirect = client.get(
        f"/{code}",
        headers=headers,
        cookies=cookies,
        params=params,
        allow_redirects=False
    )
    assert redirect.status_code == 307 or redirect.status_code == 302

    # Stats
    stats = client.get(f"/api/stats/{code}")
    assert stats.status_code == 200
    stats_data = stats.json()
    # Debe haber al menos 1 visita registrada
    assert stats_data["total_visits"] >= 1


def test_redirect_with_minimal_data():
    """Caso periférico: registrar visita sin headers ni cookies"""
    # Crear URL
    response = client.post("/api/shorten", json={"url": "https://example.com"})
    data = response.json()
    code = data["short_code"]

    # Redirigir sin headers ni cookies
    redirect = client.get(f"/{code}", allow_redirects=False)
    assert redirect.status_code == 307 or redirect.status_code == 302

    # Stats
    stats = client.get(f"/api/stats/{code}")
    assert stats.status_code == 200
    stats_data = stats.json()
    assert stats_data["total_visits"] >= 1
