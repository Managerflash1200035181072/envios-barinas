# Proyecto: Sistema Web para la Gestión de Envíos de Artículos en Barinas

## Metodología de desarrollo en V - Rama Descendente (Verificación)

### 1. Análisis de Requisitos (Requirement Gathering)

El sistema debe digitalizar y centralizar el ciclo completo de un envío de artículos en la ciudad de Barinas: desde el registro del paquete por parte del cliente, pasando por la asignación a un repartidor, el seguimiento del trayecto, hasta la confirmación de entrega y la generación de reportes.

Alcance de esta entrega: el objetivo principal de esta primera entrega es el desarrollo del módulo de autenticación y gestión de roles (`accounts`). El núcleo operativo (gestión de envíos) se implementará en entregas posteriores.

Módulos funcionales mínimos:
- Registro y autenticación con roles: Visitante, Cliente, Repartidor y Administrador.
- Gestión de envíos: creación de solicitudes con datos de remitente, destinatario, artículo, peso/dimensiones, direcciones y tipo de servicio.
- Asignación y seguimiento de repartidores: control del trayecto logístico y actualización de estados (pendiente, en tránsito, entregado, cancelado). *Nota: la geolocalización por GPS o el trazado de mapas quedan fuera del alcance.*
- Seguimiento del envío mediante código único de rastreo (accesible incluso para visitantes no autenticados), basado en el historial de estados del paquete.
- Cálculo de tarifas y registro del estado de pago (pendiente, pagado, contra entrega). Las pasarelas de pago quedan fuera del alcance.
- Notificaciones básicas dentro del sistema.
- Panel administrativo y módulo de reportes.

Fuera del alcance: pasarelas de pago en línea, facturación electrónica, reembolsos automáticos, conciliación bancaria automática y rastreo satelital/GPS en tiempo real.

### 2. Análisis del Sistema (System Analysis)

Justificación: la gestión actual en Barinas se realiza de forma manual o con herramientas dispersas (llamadas, WhatsApp, papel, hojas de cálculo), lo que provoca pérdida de información, falta de trazabilidad, errores en la asignación de repartidores, cálculo inconsistente de tarifas y ausencia de reportes confiables. El sistema digitalizará y centralizará la operación, dará transparencia al cliente, optimizará la logística y aportará al desarrollo tecnológico local de Barinas.

Arquitectura cliente-servidor. El backend expone vistas renderizadas con plantillas de Django. El frontend con Vite queda como base limpia para futuras integraciones; en esta entrega todavía no consume una API. La base de datos es SQLite.

Actores: empresas de mensajería y encomiendas locales, emprendedores y pequeños comercios, clientes finales (remitentes y destinatarios), repartidores/mensajeros, administradores y personal operativo.

### 3. Diseño de Software / Arquitectura (Software Design)

- Backend: Python 3.11 + Django 4.2 (patrón MVC/MVT).
- Frontend: Node.js 22 + Vite (bundler y servidor de desarrollo).
- Base de datos: SQLite.
- Contenedores: Docker Engine + Docker Compose.
- Control de versiones: Git + GitHub.

### 4. Diseño de Módulos (Module Design)

Módulo `accounts` - autenticación y roles (implementado en esta entrega):
- Reutiliza el modelo `User` nativo de Django.
- Roles implementados mediante Grupos de Django: Administrador, Repartidor y Cliente. El Visitante es implícito (usuario no registrado con acceso solo a vistas públicas).
- La migración `accounts/migrations/0001_crear_grupos.py` crea los grupos automáticamente al ejecutar `migrate`.
- El formulario de registro asigna el grupo Cliente por defecto a cada usuario nuevo.
- El superusuario se considera Administrador para el panel personalizado y además conserva acceso al Django Admin.
- Vistas: registro, login, logout, home pública y paneles por rol.
- Decoradores `@login_required` y `requiere_rol` para proteger las vistas según el rol.

Módulo `envios` - núcleo del negocio (pendiente por desarrollar en próximas entregas):
- Modelará Envio, HistorialEstado y Tarifa.
- Incluirá creación de envíos, asignación de repartidores, rastreo público por código (basado en el historial de estados del paquete, sin geolocalización GPS), actualización de estados, tarifas y reportes.

Módulo `core` - configuración central del proyecto (settings y URLs principales).

Módulo `frontend` - base limpia de Vite, preparada para futuras integraciones de interfaz de usuario dinámica.

### Equivalencia de roles

La nomenclatura del dominio del proyecto se mantiene y se relaciona con los roles solicitados en la consigna de la siguiente manera:

| Rol solicitado en la consigna | Rol en el proyecto |
|---|---|
| Administrador | Administrador |
| Gestor | Repartidor (rol operativo) |
| Usuario | Cliente |
| Visitante | Visitante (no autenticado) |

### 5. Punto de Inflexión: Codificación (Coding)

A partir de aquí comienza la construcción del código fuente, la dockerización, la configuración de roles y el despliegue del entorno de desarrollo. En esta primera entrega se implementa únicamente el módulo `accounts` (registro, inicio de sesión y roles); el módulo `envios` se desarrollará en la siguiente entrega.

## Puesta en marcha

### Requisitos

- Docker Engine y Docker Compose v2 (`docker compose`).
- Docker Desktop iniciado si usas Windows o macOS.
- Puertos `8000` (Django) y `5173` (Vite) libres.
- No hace falta instalar Python, Node.js ni Django en el equipo host: las dependencias se instalan dentro de los contenedores.

Todos los comandos deben ejecutarse desde la raíz del proyecto, donde se encuentra `docker-compose.yml`.

### 1. Construir y levantar los servicios

```bash
docker compose up --build -d
```

La primera ejecución puede tardar varios minutos porque descarga las imágenes y instala las dependencias. El flag `-d` deja los contenedores en segundo plano para poder ejecutar los comandos siguientes en la misma terminal.

### 2. Verificar que el backend esté listo

```bash
docker compose ps
docker compose logs -f backend
```

Cuando aparezca `Starting development server at http://0.0.0.0:8000/`, puedes salir de los logs con `Ctrl+C`. El backend debe figurar como `Up`.

### 3. Aplicar las migraciones

```bash
docker compose exec backend python manage.py migrate
```

Esto crea las tablas de SQLite y los grupos/roles `Administrador`, `Repartidor` y `Cliente`.

### 4. Crear un superusuario

```bash
docker compose exec backend python manage.py createsuperuser
```

El correo electrónico es opcional. Este usuario puede entrar a Django Admin y también al panel administrativo personalizado.

### 5. Abrir la aplicación

| Recurso | URL |
|---|---|
| Aplicación Django | <http://localhost:8000/> |
| Registro de clientes | <http://localhost:8000/registro/> |
| Inicio de sesión | <http://localhost:8000/login/> |
| Django Admin | <http://localhost:8000/admin/> |
| Panel administrativo propio | <http://localhost:8000/admin-panel/> |
| Panel Cliente | <http://localhost:8000/cliente/> |
| Panel Repartidor | <http://localhost:8000/repartidor/> |
| Frontend Vite (opcional) | <http://localhost:5173/> |

Los paneles `/cliente/`, `/repartidor/` y `/admin-panel/` requieren sesión y el rol correspondiente. El frontend de Vite es una base de trabajo y todavía no consume la API de Django; la aplicación funcional de esta entrega se encuentra en <http://localhost:8000/>.

### 6. Verificación rápida

1. Abrir <http://localhost:8000/> y confirmar que se muestra la página pública.
2. Registrarse en `/registro/` y comprobar que la cuenta queda creada como Cliente y que el panel Cliente es accesible.
3. Iniciar sesión con el superusuario en `/admin/` y confirmar el acceso a usuarios, grupos y permisos.
4. Crear o asignar un usuario al grupo `Repartidor` y probar `/repartidor/`.

### 7. Detener el proyecto

```bash
docker compose down
```

Este comando detiene y elimina los contenedores, pero conserva `backend/db.sqlite3` y los datos. Para volver a iniciar:

```bash
docker compose up -d
```

### Datos y persistencia

`backend/db.sqlite3` no se versiona. En una instalación limpia, `migrate` crea la base de datos y los roles del sistema. Si eliminas ese archivo, deberás ejecutar `migrate` y `createsuperuser` nuevamente.

## Roles de prueba

- **Cliente:** se asigna automáticamente al registrarse en `/registro/`.
- **Administrador:** se obtiene con el superusuario o asignando el grupo `Administrador` a un usuario desde Django Admin.
- **Repartidor:** se asigna desde Django Admin, en la sección de usuarios, agregando el grupo `Repartidor`.
- **Visitante:** no requiere cuenta; solo accede a la home pública y al registro/login.

Para probar un rol, entra a <http://localhost:8000/admin/>, abre el usuario y añade el grupo correspondiente en la sección de permisos/grupos.

## Problemas comunes

- **El puerto 8000 o 5173 está ocupado:** detén el proceso que los usa o cambia los puertos en `docker-compose.yml` y vuelve a levantar con `docker compose up -d`.
- **`migrate` falla porque el backend aún no está listo:** espera unos segundos, revisa `docker compose logs -f backend` y vuelve a ejecutar el comando.
- **No se ve la aplicación desde otra máquina de la red:** agrega la IP correspondiente a `ALLOWED_HOSTS` en `backend/core/settings.py` y reinicia el backend.

## Cumplimiento de las actividades B.1-B.8

| Actividad | Evidencia |
|---|---|
| B.1. Stack de desarrollo | Python 3.11, Django 4.2, Node.js 22, Vite y Docker definidos en `backend/Dockerfile`, `frontend/Dockerfile` y `docker-compose.yml`. |
| B.2. Entorno virtual con Docker | Servicios `backend` y `frontend` en `docker-compose.yml`. |
| B.3. Repositorio en GitHub | Se gestiona por separado; no forma parte de los cambios de código de esta entrega. |
| B.4. Django y librerías | `backend/requirements.txt` con `Django==4.2.30`. |
| B.5. Backend estructurado | Proyecto `core` y aplicación `accounts` dentro de `backend/`. |
| B.6. App de registro e inicio de sesión | `backend/accounts/` con vistas, formularios, URLs y plantillas de registro, login y logout. |
| B.7. Django Admin configurado | `backend/accounts/admin.py` con administración personalizada de usuarios y grupos/roles. |
| B.8. Vistas por roles | Home público, paneles de Cliente, Repartidor y Administrador, protegidos con `@login_required` y `requiere_rol`. |
