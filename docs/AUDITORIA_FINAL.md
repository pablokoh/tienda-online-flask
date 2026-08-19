# Auditoría final — Proyecto Tienda Online

Esta auditoría contrasta el contenido preparado para entrega con la actividad **Proyecto Tienda Online (Flask + PostgreSQL)**.

## Parte 1 — Tutorial

| Requisito | Estado | Evidencia en el proyecto |
|---|---|---|
| PostgreSQL configurable | Cumple en código | `config.py` construye `SQLALCHEMY_DATABASE_URI` desde `.env`. La conexión real debe probarse en el equipo de entrega. |
| Entorno virtual / dependencias | Cumple | `requirements.txt` y pasos en `README.md`. |
| `Producto` + herencia POO | Cumple | `models.py`: `ProductoFisico`, `ProductoDigital`, `ProductoPerecible`. |
| Polimorfismo | Cumple | Cada subtipo sobreescribe `precio_final()`. |
| Plantillas base y catálogo | Cumple | Archivos dentro de `templates/`; `base.html` + `index.html`. |
| CRUD completo | Cumple | Crear por subtipo, consultar, editar campos generales y específicos, desactivación lógica. |
| Login | Cumple | Registro, login y logout en `app.py`. |
| Contraseñas con hash | Cumple | `generate_password_hash` y `check_password_hash`. |
| Roles | Cumple | `Usuario.rol`, sesión y controles por admin. |
| `login_requerido` | Cumple | Decorador implementado en `app.py`. |
| `rol_requerido` | Cumple | Decorador implementado y aplicado a CRUD administrativo. |
| Protección de rutas | Cumple | Crear, editar y eliminar requieren sesión y rol `admin`. |
| Carrito funcional | Cumple | Agregar, listar, actualizar, eliminar y vaciar; cantidades limitadas por stock. |

## Parte 2A — Subida de imágenes

| Requisito | Estado | Evidencia |
|---|---|---|
| Campo de imagen en `Producto` | Cumple | `imagen = db.Column(...)` en `models.py`. |
| Migración de BD | Preparada | `migraciones/001_agregar_imagen.sql`. Debe ejecutarse contra la BD existente. |
| `<input type="file">` | Cumple | Parcial reutilizable `_campo_imagen.html`. |
| `multipart/form-data` | Cumple | Formularios de creación y edición. |
| `request.files` | Cumple | Procesamiento en `app.py`. |
| `secure_filename` | Cumple | Importado y aplicado antes de guardar. |
| Guardado en `static/uploads/` | Cumple | `guardar_imagen()`. |
| Imagen en catálogo | Cumple | `index.html`. |
| Imagen en detalle | Cumple | `detalle.html`. |
| Imagen por defecto | Cumple | `default_product.svg`. |
| Validación básica de imágenes | Cumple | Extensiones permitidas + tamaño máximo de 5 MB. |

## Parte 2B — Diseño

| Requisito | Estado | Evidencia |
|---|---|---|
| Bootstrap incluido | Cumple | Bootstrap 5.3.3 en `base.html`. |
| Catálogo mejorado | Cumple | Cards, imagen, badges, precio, stock, estados hover y layout responsive. |
| Identidad visual | Cumple | Marca `Puentes Shop`, CSS propio y paleta coherente. |
| Íconos | Cumple | Bootstrap Icons. |
| Navegación responsive | Cumple | Navbar con `navbar-toggler`. |
| Feedback con `flash()` | Cumple | Alertas Bootstrap en `base.html`. |

## Preparación para GitHub

| Requisito | Estado |
|---|---|
| `.gitignore` | Cumple |
| `.env` fuera de la entrega | Cumple |
| `.env.example` | Cumple |
| `requirements.txt` | Cumple |
| `README.md` con instalación | Cumple |
| Pasos de PostgreSQL | Cumple |
| Pasos de migración | Cumple |
| Pasos de GitHub | Cumple |

## Lo que todavía debe verificarse en tu computadora

El código y la estructura pueden auditarse sin una base PostgreSQL activa, pero estos puntos requieren ejecución local:

1. Crear o conectar la base `tienda_online` con tus credenciales reales.
2. Copiar `.env.example` a `.env` y colocar la contraseña correcta.
3. Si partes de una BD antigua, ejecutar `migraciones/001_agregar_imagen.sql`.
4. Ejecutar `python init_db.py` si la base está vacía.
5. Ejecutar `python crear_admin.py` para disponer de un usuario administrador.
6. Iniciar `python app.py` y completar las pruebas del README.
7. Revisar visualmente que las cuatro imágenes de demostración carguen correctamente en el navegador.
8. Guardar las capturas reales en `docs/capturas/` siguiendo la guía incluida.
9. Hacer `git add`, `commit` y `push` de las correcciones y evidencias.
10. Confirmar en GitHub que **`.env` no fue publicado**.

## Observaciones fuera del alcance solicitado

No se implementan pagos, pedidos persistentes, checkout, CSRF avanzado, almacenamiento en nube ni panel de administración separado porque no forman parte de la actividad indicada. Para una aplicación productiva serían mejoras recomendables, pero **no son necesarias para cumplir esta entrega académica**.

## Veredicto técnico

A nivel de código y estructura, el proyecto queda preparado para cubrir los requisitos descritos de Semanas 1, 2 y 3, la mejora de subida de imágenes y la mejora visual. El único punto que no puede certificarse sin el entorno local es la **integración efectiva con tu instancia de PostgreSQL y la prueba end-to-end en navegador**.

## Evidencias visuales recomendadas

La consigna funcional queda cubierta por el código, pero para una entrega académica se recomienda acompañarla con evidencia de ejecución real. La guía completa está en `docs/capturas/README.md`.

Las evidencias prioritarias son: catálogo con imágenes, detalle, cliente, administrador, subida de imagen, carrito, control de permisos y PostgreSQL.
