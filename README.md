# Puentes Shop — Tienda Online Flask + PostgreSQL

Proyecto académico de una tienda online desarrollado con **Flask**, **PostgreSQL**, **SQLAlchemy** y **Bootstrap**.

## Funcionalidades

- POO con herencia y polimorfismo: `Producto`, `ProductoFisico`, `ProductoDigital` y `ProductoPerecible`.
- CRUD completo de productos.
- Registro, login y logout con contraseñas encriptadas.
- Roles `cliente` y `admin` con rutas protegidas.
- Carrito de compras mediante sesión.
- Subida de imágenes con `request.files` y `secure_filename`.
- Imagen predeterminada para productos sin fotografía.
- Mensajes `flash()` con alertas de Bootstrap.
- Diseño responsive con Bootstrap 5.

## Instalación

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copia `.env.example` como `.env` y configura tu conexión a PostgreSQL:

```env
DB_USER=postgres
DB_PASSWORD=TU_PASSWORD
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tienda_online
SECRET_KEY=TU_CLAVE_SECRETA
```

Crea la base de datos:

```sql
CREATE DATABASE tienda_online;
```

Si es una base nueva:

```powershell
python init_db.py
```

Si ya existe una base anterior, aplica la migración:

```powershell
psql -U postgres -d tienda_online -f migraciones/001_agregar_imagen.sql
```

## Administrador

```powershell
python crear_admin.py
```

Los usuarios registrados desde la web reciben el rol `cliente`. El script permite crear un usuario con rol `admin`.

## Ejecutar

```powershell
python app.py
```

Abrir:

```text
http://127.0.0.1:5000
```

## Evidencias

Las capturas de funcionamiento pueden guardarse en `docs/capturas/`, incluyendo catálogo, detalle de producto, administrador, carrito, subida de imágenes, permisos y PostgreSQL.

## Seguridad

El archivo `.env` contiene credenciales locales y **no debe subirse a GitHub**. El proyecto incluye `.env.example` y `.gitignore`.
