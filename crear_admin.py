from getpass import getpass

from app import app
from models import Usuario, db


with app.app_context():
    db.create_all()

    nombre = input("Nombre del administrador: ").strip()
    email = input("Correo del administrador: ").strip().lower()
    password = getpass("Contraseña (mínimo 6 caracteres): ")

    if not nombre or not email or len(password) < 6:
        raise SystemExit("Datos inválidos. Revisa nombre, correo y contraseña.")

    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        usuario.nombre = nombre
        usuario.rol = "admin"
        usuario.set_password(password)
        mensaje = "Usuario existente actualizado como administrador."
    else:
        usuario = Usuario(nombre=nombre, email=email, rol="admin")
        usuario.set_password(password)
        db.session.add(usuario)
        mensaje = "Administrador creado correctamente."

    db.session.commit()
    print(mensaje)
