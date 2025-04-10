# TASK.MD - Tareas Iniciales del Proyecto

## Fase 1: Configuración del Entorno de Desarrollo

### 1.1 Preparación del Entorno
- [x] Crear un repositorio Git para el proyecto
- [x] Configurar un entorno virtual Python (venv o conda)
- [x] Crear archivo `requirements.txt` con dependencias iniciales
- [x] Configurar estructura básica de carpetas del proyecto

### 1.2 Instalación de Dependencias Básicas
```
pip install flask
pip install flask-sqlalchemy
pip install python-dotenv
pip install wtforms
```

## Fase 2: Desarrollo del Backend Básico

### 2.1 Configuración de la Base de Datos
- [x] Crear modelos para URL y Visitas
- [x] Configurar SQLAlchemy y crear script de inicialización de BD
- [x] Implementar funciones CRUD básicas para URLs

### 2.2 Desarrollo de la Lógica Principal
- [x] Implementar generador de códigos cortos
- [x] Crear función para validar URLs de entrada
- [x] Implementar sistema de redirección con captura de IP
- [x] Desarrollar mecanismo de almacenamiento de IPs y datos de visita

### 2.3 Desarrollo de API REST Básica
- [x] Crear endpoint para acortar URLs (`/api/shorten`)
- [x] Crear endpoint de redirección (`/<short_code>`)
- [x] Crear endpoint para estadísticas (`/api/stats/<short_code>`)

## Fase 3: Desarrollo del Frontend Básico

### 3.1 Interfaz Principal
- [x] Diseñar y desarrollar página principal con formulario
- [x] Implementar JavaScript para envío asíncrono del formulario
- [x] Diseñar visualización de URL acortada y opciones para compartir

### 3.2 Panel de Administración
- [x] Crear página de inicio de sesión
- [x] Diseñar dashboard para visualizar URLs y estadísticas
- [x] Implementar tabla/lista de IPs capturadas por URL

## Fase 4: Seguridad y Autenticación

### 4.1 Sistema de Autenticación
- [x] Implementar registro y login de usuarios
- [x] Configurar sistema de sesiones
- [x] Proteger rutas de administración

### 4.2 Medidas de Seguridad
- [x] Implementar validación y sanitización de entradas
- [x] Configurar rate limiting básico
- [x] Implementar CSRF protection

## Fase 5: Pruebas Iniciales

### 5.1 Pruebas Unitarias
- [x] Escribir tests para el generador de códigos cortos
- [x] Escribir tests para el sistema de redirección
- [x] Escribir tests para la API REST

### 5.2 Pruebas Manuales
- [x] Probar flujo completo de acortamiento de URL
- [x] Verificar captura correcta de IP
- [x] Probar panel de administración

---

## Guía para Pruebas Manuales

### Flujo de acortamiento
1. Accede a `http://localhost:8000/static/index.html`.
2. Ingresa una URL válida y presiona "Acortar".
3. Verifica que se muestre un enlace corto.
4. Accede al enlace corto y confirma que redirige correctamente.

### Captura de IP
1. Accede varias veces al enlace corto desde diferentes dispositivos o IPs.
2. Consulta `/api/stats/<short_code>` y verifica que las IPs y timestamps se registren correctamente.

### Panel de administración
1. Accede a `http://localhost:8000/static/admin.html`.
2. Inicia sesión (simulado).
3. Verifica que se muestren las URLs acortadas.
4. Haz clic en el contador de visitas para ver la tabla de IPs y fechas.

## Fase 6: Preparación para Despliegue Inicial

### 6.1 Configuración de Entorno
- [ ] Crear archivo `.env.example` con variables de entorno necesarias
- [ ] Documentar proceso de configuración
- [ ] Configurar diferentes entornos (desarrollo/producción)

### 6.2 Documentación
- [ ] Actualizar README con instrucciones de instalación y uso
- [ ] Documentar API para desarrolladores
- [ ] Crear manual básico de usuario

## Próximos Pasos (Para Fases Futuras)

- Implementar análisis básico de datos (gráficos, tendencias)
- Mejorar UX/UI del panel de administración
- Añadir funcionalidades como expiración de enlaces
- Implementar geolocalización básica de IPs
- Configurar sistema de alertas para detección de abusos

## Detectadas durante el trabajo

- [x] 09/04/2025 - Ejecutar el proyecto dentro del entorno virtual (crear, instalar dependencias y correr servidor)
- [ ] 09/04/2025 - Ampliar la captura de detalles de visitas para incluir información de red (tipo de conexión, proxy, VPN), agente de usuario detallado, cookies y parámetros adicionales si se usan scripts complejos.
- [ ] 10/04/2025 - Configurar correctamente la cadena `DATABASE_URL` con la URL PostgreSQL de Supabase para que los datos se almacenen allí y no en SQLite local.
