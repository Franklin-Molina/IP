from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Visit(Base):
    """
    Modelo para representar una visita a una URL acortada.
    """
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"))
    ip_address = Column(String)
    user_agent = Column(String(512), nullable=True)
    referrer = Column(String(512), nullable=True)
    network_info = Column(Text, nullable=True)  # JSON o texto con info de red
    cookies = Column(Text, nullable=True)       # JSON o texto con cookies
    extra_params = Column(Text, nullable=True)  # JSON o texto con parámetros adicionales
    device_info = Column(String(256), nullable=True)  # Sistema operativo y navegador
    latitude = Column(String(20), nullable=True)  # Latitud
    longitude = Column(String(20), nullable=True)  # Longitud
    isp = Column(String(256), nullable=True)  # ISP
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    url = relationship("URL", backref="visits")
