<<<<<<< HEAD
# Puentes shop — Tienda Online con Flask + PostgreSQL
=======
# Puentes Shop — Tienda Online con Flask + PostgreSQL
>>>>>>> 744c6a7 (Correcines  Finales)

Proyecto académico de una tienda online desarrollado con **Flask**, **PostgreSQL**, **SQLAlchemy**, **POO con herencia y polimorfismo**, autenticación de usuarios, roles, CRUD de productos, carrito de compras y carga de imágenes.

## Funcionalidades implementadas

- Catálogo de productos activos.
- Detalle individual de cada producto.
- Jerarquía POO: `Producto`, `ProductoFisico`, `ProductoDigital` y `ProductoPerecible`.
- Polimorfismo mediante `precio_final()` según el tipo de producto.
- CRUD de productos para administradores.
- Registro, login y logout.
- Contraseñas almacenadas con hash de Werkzeug.
- Decoradores `login_requerido` y `rol_requerido`.
- Rutas administrativas protegidas por rol.
- Carrito de compras guardado en la sesión de Flask.
- Subida de imágenes mediante `request.files` y `secure_filename`.
- Validación de extensiones y límite de 5 MB por imagen.
- Imagen predeterminada cuando un producto no tiene fotografía.
- Bootstrap 5 + Bootstrap Icons + estilos propios.
- Mensajes `flash()` presentados como alertas de Bootstrap.
- Migración SQL manual para agregar la columna `imagen` a una base creada previamente.

## Estructura del proyecto

```text
Tienda_Online_Entrega/
├── app.py
├── config.py
├── models.py
├── init_db.py
├── crear_admin.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── migraciones/
│   └── 001_agregar_imagen.sql
├── docs/
│   ├── AUDITORIA_FINAL.md
│   └── capturas/
│       └── README.md
├── static/
│   ├── css/
│   │   └── styles.css
│   └── uploads/
│       ├── default_product.svg
│       ├── pc_gaming_pablo.jpg
│       ├── teclado_gaming.png
│       ├── logitech_g502_x.png
│       └── silla_gamer.png
└── templates/
    ├── base.html
    ├── index.html
    ├── detalle.html
    ├── editar.html
    ├── carrito.html
    ├── login.html
    ├── registro.html
    ├── nuevo_fisico.html
    ├── nuevo_digital.html
    ├── nuevo_perecible.html
    ├── _campo_imagen.html
    └── 404.html
```

---

# Instalación paso a paso

## 1. Requisitos

Antes de ejecutar el proyecto necesitas:

- Python 3.10 o superior.
- PostgreSQL instalado y ejecutándose.
- Git, únicamente si vas a subir el proyecto a GitHub.

Comprueba Python con:

```bash
python --version
```

## 2. Crear y activar el entorno virtual

Desde la carpeta del proyecto:

### Windows CMD

```bash
python -m venv venv
venv\Scripts\activate
```

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

## 4. Crear el archivo `.env`

Copia `.env.example` y renómbralo a `.env`.

En Windows CMD:

```bash
copy .env.example .env
```

En macOS/Linux:

```bash
cp .env.example .env
```

Edita `.env` con los datos reales de tu PostgreSQL:

```env
DB_USER=postgres
DB_PASSWORD=TU_PASSWORD_REAL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tienda_online
SECRET_KEY=UNA_CLAVE_LARGA_Y_ALEATORIA
```

**Nunca subas `.env` a GitHub.** Ya está incluido en `.gitignore`.

## 5. Enlazar PostgreSQL

Crea la base de datos desde PostgreSQL o pgAdmin:

```sql
CREATE DATABASE tienda_online;
```

Después asegúrate de que los valores de `.env` coincidan con tu instalación.

### Si la base está vacía

Ejecuta:

```bash
python init_db.py
```

`init_db.py` ejecuta `db.create_all()` y agrega productos de demostración únicamente si la tabla de productos está vacía. **No elimina datos existentes.**

### Si ya tienes la base de las semanas anteriores

La mejora de imágenes agrega una nueva columna. Ejecuta la migración:

```bash
psql -U postgres -d tienda_online -f migraciones/001_agregar_imagen.sql
```

También puedes abrir el archivo `migraciones/001_agregar_imagen.sql` en pgAdmin y ejecutarlo desde Query Tool.

## 6. Crear un administrador

Los usuarios registrados desde la web reciben el rol `cliente` de forma predeterminada. Para crear el primer administrador:

```bash
python crear_admin.py
```

El script solicitará nombre, correo y contraseña sin guardar credenciales en el repositorio.

## 7. Ejecutar la aplicación

```bash
python app.py
```

Después abre en el navegador:

```text
http://127.0.0.1:5000
```

---

# Pruebas recomendadas antes de entregar

1. Abrir `/` y comprobar que el catálogo carga.
2. Abrir el detalle de un producto.
3. Registrar un usuario nuevo.
4. Iniciar sesión como cliente y verificar que no aparecen controles administrativos.
5. Intentar abrir manualmente `/productos/nuevo/fisico` como cliente; debe negar el acceso.
6. Iniciar sesión como administrador.
7. Crear un producto físico con imagen.
8. Crear un producto digital sin imagen y comprobar que usa la imagen por defecto.
9. Editar el producto y cambiar su imagen.
10. Desactivar un producto y verificar que desaparece del catálogo.
11. Iniciar sesión como cliente, agregar varios productos al carrito, actualizar cantidades y eliminar productos.
12. Cerrar sesión y comprobar que la sesión se limpia.

---


# Evidencias para la entrega

La carpeta [`docs/capturas/`](docs/capturas/) está preparada para guardar las capturas reales de ejecución. Las capturas no se falsifican ni se generan desde el código: deben realizarse con Flask y PostgreSQL funcionando en tu equipo.

Evidencias recomendadas:

- Catálogo mostrando las imágenes correctamente.
- Detalle de producto.
- Sesión como cliente.
- Sesión como administrador.
- Creación o edición de producto con carga de imagen.
- Carrito con productos y total.
- Protección de una ruta administrativa frente a un cliente.
- Consulta de PostgreSQL mostrando `tipo` e `imagen`.

Consulta [`docs/capturas/README.md`](docs/capturas/README.md) para los nombres exactos de archivo y las consultas SQL sugeridas.

---

# Subir correctamente a GitHub

Antes del primer commit, verifica que **`.env` no aparezca** en los archivos a subir.

```bash
git init
git status
git add .
git status
git commit -m "Proyecto final tienda online Flask PostgreSQL"
git branch -M main
git remote add origin URL_DE_TU_REPOSITORIO
git push -u origin main
```

Para comprobar que `.env` está ignorado:

```bash
git check-ignore -v .env
```

Debe indicar que la regla proviene de `.gitignore`.

Si `.env` se hubiera agregado accidentalmente antes de crear `.gitignore`, retíralo del índice sin borrarlo de tu PC:

```bash
git rm --cached .env
```

Después vuelve a hacer commit.

---


## Actualizar un repositorio de GitHub ya creado

Si el repositorio remoto ya está configurado, después de copiar estas correcciones y las capturas ejecuta:

```bash
git status
git add .
git commit -m "Correcciones finales y evidencias de entrega"
git push
```

Comprueba en GitHub que `.env`, `venv/` y `__pycache__/` no hayan sido publicados.

# Roles y permisos

| Acción | Visitante | Cliente | Admin |
|---|---:|---:|---:|
| Ver catálogo | Sí | Sí | Sí |
| Ver detalle | Sí | Sí | Sí |
| Registrarse / login | Sí | Sí | Sí |
| Usar carrito | No | Sí | Sí |
| Crear producto | No | No | Sí |
| Editar producto | No | No | Sí |
| Desactivar producto | No | No | Sí |

La protección importante se realiza **en las rutas de Flask**, no únicamente ocultando botones en HTML.

# Carga de imágenes

Los formularios usan:

```html
<form method="post" enctype="multipart/form-data">
<input type="file" name="imagen">
```

Flask procesa el archivo con `request.files`; el nombre recibido pasa por `werkzeug.utils.secure_filename`, se valida la extensión y se guarda en `static/uploads/` con un nombre único.

Extensiones permitidas: `png`, `jpg`, `jpeg` y `webp`.

# Notas técnicas

- El carrito es académico y se almacena en la sesión; no implementa pago ni creación de pedidos porque la actividad solicitada llega hasta carrito funcional.
- La eliminación de productos es lógica: se establece `activo = False` en vez de borrar físicamente la fila.
- Las imágenes de demostración incluidas en `static/uploads/` provienen de los recursos preparados para esta entrega.
- `debug=True` se conserva en `app.py` para desarrollo local; no debe usarse así en producción.

## Auditoría

Consulta [`docs/AUDITORIA_FINAL.md`](docs/AUDITORIA_FINAL.md) para el contraste final con la consigna y los puntos que todavía requieren verificación local.
