# PLANNING.MD - Sistema Acortador de URLs con Captura de IP

## Descripción del Proyecto
Desarrollar un sistema web que permita a los usuarios:
1. Ingresar una URL larga
2. Generar una versión acortada de esa URL
3. Capturar la dirección IP de los visitantes que utilizan los enlaces acortados
4. Almacenar y visualizar esta información a través de un panel de administración

## Alcance (Scope)
### Incluido:
- Sistema web para acortar URLs
- Mecanismo de redirección que captura la IP del visitante
- Almacenamiento de datos (URLs e IPs)
- Panel de administración básico para visualizar estadísticas
- Autenticación simple para el panel de administración

### Excluido:
- Análisis avanzado de datos de visitantes
- Geolocalización de IPs
- Integración con servicios externos de análisis
- Personalización de URLs acortadas

## Arquitectura Técnica

### Backend:
- **Lenguaje**: Python
- **Framework Web**: Flask o FastAPI
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **ORM**: SQLAlchemy

### Frontend:
- **Framework**: Bootstrap básico para UI responsiva
- **JavaScript**: Vanilla JS o jQuery para interacciones básicas
- **Plantillas**: Jinja2 (si se usa Flask)

### Despliegue:
- Desarrollo local: Servidor de desarrollo de Flask/FastAPI
- Producción: Gunicorn + Nginx (opcional)

## Consideraciones de Seguridad
- Autenticación para el panel de administración
- Validación de URLs de entrada
- Sanitización de datos
- Limitación de tasas (rate limiting) para prevenir abusos
- Consideraciones sobre privacidad y datos personales (GDPR)

## Estructura de Datos

### Tabla de URLs
- `id`: Identificador único
- `original_url`: URL original completa
- `short_code`: Código corto generado
- `created_at`: Fecha y hora de creación
- `user_id`: Referencia al usuario que creó el enlace (si aplica)

### Tabla de Visitas
- `id`: Identificador único
- `url_id`: Referencia a la URL acortada
- `ip_address`: Dirección IP del visitante
- `user_agent`: Información del navegador/dispositivo (opcional)
- `visited_at`: Fecha y hora de la visita
- `referrer`: URL de origen (opcional)

## Flujo de Trabajo
1. Usuario ingresa URL larga en la interfaz web
2. Sistema valida la URL
3. Sistema genera un código corto único
4. Sistema almacena la URL original y su código corto
5. Sistema devuelve la URL acortada al usuario
6. Cuando un visitante accede a la URL acortada:
   - Sistema captura la IP y datos relevantes
   - Sistema redirecciona al visitante a la URL original
7. Administrador puede ver estadísticas en el panel de administración

## Riesgos y Mitigaciones
- **Alto tráfico**: Implementar caché y optimizar consultas a la base de datos
- **Abuso del sistema**: Implementar rate limiting y captcha
- **Problemas legales**: Revisar implicaciones legales de almacenar IPs (considerar GDPR)
- **Enlaces maliciosos**: Implementar verificación de URLs

## Recursos Necesarios
- Servidor web para despliegue
- Dominio corto (opcional para URLs más compactas)
- Espacio de almacenamiento para la base de datos