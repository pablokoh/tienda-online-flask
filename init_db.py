"""Crea las tablas y agrega productos de demostración si la base está vacía.

Este script NO borra tablas ni datos existentes.
"""

from app import app
from models import db, Producto, ProductoDigital, ProductoFisico, ProductoPerecible


with app.app_context():
    db.create_all()
    print("Tablas verificadas/creadas correctamente.")

    if Producto.query.count() == 0:
        productos = [
            ProductoFisico(
                codigo="FIS001",
                nombre="PC Gaming",
                precio_base=1250.00,
                stock=6,
                peso_kg=8.0,
                costo_envio_por_kg=1.50,
                imagen="pc_gaming_pablo.jpg",
            ),
            ProductoFisico(
                codigo="FIS002",
                nombre="Teclado Gaming",
                precio_base=79.99,
                stock=18,
                peso_kg=0.9,
                costo_envio_por_kg=1.50,
                imagen="teclado_gaming.png",
            ),
            ProductoFisico(
                codigo="FIS003",
                nombre="Logitech G502 X",
                precio_base=89.99,
                stock=12,
                peso_kg=0.25,
                costo_envio_por_kg=1.50,
                imagen="logitech_g502_x.png",
            ),
            ProductoFisico(
                codigo="FIS004",
                nombre="Silla Gamer",
                precio_base=219.00,
                stock=5,
                peso_kg=17.0,
                costo_envio_por_kg=1.50,
                imagen="silla_gamer.png",
            ),
            ProductoDigital(
                codigo="DIG001",
                nombre="Curso de Python Avanzado",
                precio_base=40.00,
                stock=999,
                licencia="personal",
                imagen="default_product.svg",
            ),
            ProductoPerecible(
                codigo="PER001",
                nombre="Caja de fresas orgánicas",
                precio_base=8.00,
                stock=15,
                dias_para_vencer=2,
                imagen="default_product.svg",
            ),
        ]
        db.session.add_all(productos)
        db.session.commit()
        print("Productos de demostración insertados.")
    else:
        print("La tabla productos ya tiene datos; no se insertaron ejemplos.")
