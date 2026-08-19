# Evidencias de funcionamiento

Esta carpeta está preparada para guardar las capturas reales de la aplicación antes de la entrega.

Usa estos nombres para mantener la evidencia ordenada:

1. `01_catalogo.png` — catálogo principal con varios productos e imágenes visibles.
2. `02_detalle_producto.png` — detalle de un producto mostrando imagen, tipo, precio y stock.
3. `03_login_cliente.png` — sesión iniciada como cliente, sin controles administrativos.
4. `04_admin.png` — sesión iniciada como administrador con el menú de creación de productos.
5. `05_subida_imagen.png` — creación o edición de un producto mostrando la selección/carga de una imagen y el resultado.
6. `06_carrito.png` — carrito con al menos dos productos, cantidades y total.
7. `07_permisos.png` — intento de un cliente de acceder a una ruta administrativa y mensaje de acceso denegado.
8. `08_postgresql.png` — pgAdmin o Query Tool mostrando productos y las columnas `tipo` e `imagen`.
9. `09_usuarios_roles.png` — opcional: tabla `usuarios` mostrando al menos un `cliente` y un `admin` (sin mostrar `password_hash`).

## Consulta recomendada para la captura de productos

```sql
SELECT id, codigo, nombre, tipo, precio_base, stock, imagen
FROM productos
ORDER BY id;
```

## Consulta opcional para roles

```sql
SELECT id, nombre, email, rol
FROM usuarios
ORDER BY id;
```

No incluyas en las capturas contraseñas, contenido del archivo `.env` ni valores sensibles.
