import os
from functools import wraps
from uuid import uuid4

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from config import Config
from models import db, Producto, ProductoDigital, ProductoFisico, ProductoPerecible, Usuario


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
DEFAULT_IMAGE = "default_product.svg"

app = Flask(__name__)
app.config.from_object(Config)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
db.init_app(app)


LEGACY_IMAGE_NAMES = {
    "chuldesillasgamer.png": "silla_gamer.png",
    "logitech g502 x.png": "logitech_g502_x.png",
    "pcgaming pablo.jpg": "pc_gaming_pablo.jpg",
    "umatecladogaming.png": "teclado_gaming.png",
}


def resolver_imagen(nombre_archivo):
    """Retorna una imagen existente o la imagen predeterminada.

    También reconoce los nombres originales de los recursos usados durante
    la preparación del proyecto para evitar imágenes rotas si una base
    anterior conservó esos nombres.
    """
    if not nombre_archivo:
        return DEFAULT_IMAGE

    nombre = os.path.basename(str(nombre_archivo).strip())
    candidatos = [nombre]
    normalizado = secure_filename(nombre)
    if normalizado and normalizado not in candidatos:
        candidatos.append(normalizado)

    legado = LEGACY_IMAGE_NAMES.get(nombre.lower())
    if legado:
        candidatos.append(legado)

    for candidato in candidatos:
        ruta = os.path.join(app.config["UPLOAD_FOLDER"], candidato)
        if os.path.isfile(ruta):
            return candidato

    return DEFAULT_IMAGE


def login_requerido(vista):
    """Exige una sesión iniciada antes de ejecutar una vista."""

    @wraps(vista)
    def decorada(*args, **kwargs):
        if not session.get("usuario_id"):
            flash("Debes iniciar sesión para acceder a esta opción.", "warning")
            return redirect(url_for("login", siguiente=request.path))
        return vista(*args, **kwargs)

    return decorada


def rol_requerido(*roles_permitidos):
    """Restringe una vista a uno o más roles."""

    def decorador(vista):
        @wraps(vista)
        def decorada(*args, **kwargs):
            if not session.get("usuario_id"):
                flash("Debes iniciar sesión para acceder a esta opción.", "warning")
                return redirect(url_for("login"))
            if session.get("usuario_rol") not in roles_permitidos:
                flash("No tienes permisos para realizar esta acción.", "danger")
                return redirect(url_for("inicio"))
            return vista(*args, **kwargs)

        return decorada

    return decorador


def extension_permitida(nombre_archivo):
    return "." in nombre_archivo and nombre_archivo.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def guardar_imagen(archivo):
    """Valida, sanitiza y guarda una imagen. Retorna su nombre final."""
    if not archivo or not archivo.filename:
        return None

    nombre_seguro = secure_filename(archivo.filename)
    if not nombre_seguro or not extension_permitida(nombre_seguro):
        raise ValueError("La imagen debe ser PNG, JPG, JPEG o WEBP.")

    extension = nombre_seguro.rsplit(".", 1)[1].lower()
    nombre_final = f"{uuid4().hex}.{extension}"
    ruta = os.path.join(app.config["UPLOAD_FOLDER"], nombre_final)
    archivo.save(ruta)
    return nombre_final


def leer_numero(nombre, tipo=float, minimo=0):
    valor = tipo(request.form[nombre])
    if valor < minimo:
        raise ValueError(f"{nombre} no puede ser menor que {minimo}.")
    return valor


def obtener_carrito():
    carrito = session.get("carrito", {})
    return carrito if isinstance(carrito, dict) else {}


def construir_lineas_carrito():
    carrito = obtener_carrito()
    lineas = []
    total = 0.0
    ids_invalidos = []

    for producto_id_texto, cantidad in carrito.items():
        try:
            producto_id = int(producto_id_texto)
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            ids_invalidos.append(producto_id_texto)
            continue

        producto = db.session.get(Producto, producto_id)
        if not producto or not producto.activo or cantidad <= 0:
            ids_invalidos.append(producto_id_texto)
            continue

        cantidad = min(cantidad, producto.stock)
        subtotal = producto.precio_final() * cantidad
        total += subtotal
        lineas.append({"producto": producto, "cantidad": cantidad, "subtotal": subtotal})

    if ids_invalidos:
        for clave in ids_invalidos:
            carrito.pop(clave, None)
        session["carrito"] = carrito
        session.modified = True

    return lineas, total


@app.context_processor
def datos_globales():
    cantidad_carrito = sum(int(cantidad) for cantidad in obtener_carrito().values())
    return {"cantidad_carrito": cantidad_carrito, "resolver_imagen": resolver_imagen}


@app.route("/")
def inicio():
    productos = Producto.query.filter_by(activo=True).order_by(Producto.id.desc()).all()
    return render_template("index.html", productos=productos)


@app.route("/producto/<int:producto_id>")
def detalle_producto(producto_id):
    producto = Producto.query.filter_by(id=producto_id, activo=True).first_or_404()
    return render_template("detalle.html", producto=producto)


@app.route("/productos/nuevo/fisico", methods=["GET", "POST"])
@login_requerido
@rol_requerido("admin")
def nuevo_producto_fisico():
    if request.method == "POST":
        imagen_guardada = None
        try:
            imagen_guardada = guardar_imagen(request.files.get("imagen"))
            producto = ProductoFisico(
                codigo=request.form["codigo"].strip().upper(),
                nombre=request.form["nombre"].strip(),
                precio_base=leer_numero("precio_base", float, 0),
                stock=leer_numero("stock", int, 0),
                peso_kg=leer_numero("peso_kg", float, 0),
                costo_envio_por_kg=leer_numero("costo_envio_por_kg", float, 0),
                imagen=imagen_guardada or DEFAULT_IMAGE,
            )
            db.session.add(producto)
            db.session.commit()
            flash(f"Producto físico '{producto.nombre}' creado correctamente.", "success")
            return redirect(url_for("detalle_producto", producto_id=producto.id))
        except ValueError as error:
            flash(str(error), "danger")
        except Exception:
            db.session.rollback()
            flash("No se pudo crear el producto. Verifica que el código no esté repetido.", "danger")

    return render_template("nuevo_fisico.html")


@app.route("/productos/nuevo/digital", methods=["GET", "POST"])
@login_requerido
@rol_requerido("admin")
def nuevo_producto_digital():
    if request.method == "POST":
        try:
            imagen = guardar_imagen(request.files.get("imagen")) or DEFAULT_IMAGE
            licencia = request.form["licencia"]
            if licencia not in ProductoDigital.MULTIPLICADORES:
                raise ValueError("Selecciona un tipo de licencia válido.")

            producto = ProductoDigital(
                codigo=request.form["codigo"].strip().upper(),
                nombre=request.form["nombre"].strip(),
                precio_base=leer_numero("precio_base", float, 0),
                stock=leer_numero("stock", int, 0),
                licencia=licencia,
                imagen=imagen,
            )
            db.session.add(producto)
            db.session.commit()
            flash(f"Producto digital '{producto.nombre}' creado correctamente.", "success")
            return redirect(url_for("detalle_producto", producto_id=producto.id))
        except ValueError as error:
            flash(str(error), "danger")
        except Exception:
            db.session.rollback()
            flash("No se pudo crear el producto. Verifica que el código no esté repetido.", "danger")

    return render_template("nuevo_digital.html")


@app.route("/productos/nuevo/perecible", methods=["GET", "POST"])
@login_requerido
@rol_requerido("admin")
def nuevo_producto_perecible():
    if request.method == "POST":
        try:
            imagen = guardar_imagen(request.files.get("imagen")) or DEFAULT_IMAGE
            producto = ProductoPerecible(
                codigo=request.form["codigo"].strip().upper(),
                nombre=request.form["nombre"].strip(),
                precio_base=leer_numero("precio_base", float, 0),
                stock=leer_numero("stock", int, 0),
                dias_para_vencer=leer_numero("dias_para_vencer", int, 0),
                imagen=imagen,
            )
            db.session.add(producto)
            db.session.commit()
            flash(f"Producto perecible '{producto.nombre}' creado correctamente.", "success")
            return redirect(url_for("detalle_producto", producto_id=producto.id))
        except ValueError as error:
            flash(str(error), "danger")
        except Exception:
            db.session.rollback()
            flash("No se pudo crear el producto. Verifica que el código no esté repetido.", "danger")

    return render_template("nuevo_perecible.html")


@app.route("/producto/<int:producto_id>/editar", methods=["GET", "POST"])
@login_requerido
@rol_requerido("admin")
def editar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)

    if request.method == "POST":
        try:
            producto.nombre = request.form["nombre"].strip()
            producto.precio_base = leer_numero("precio_base", float, 0)
            producto.stock = leer_numero("stock", int, 0)

            if isinstance(producto, ProductoFisico):
                producto.peso_kg = leer_numero("peso_kg", float, 0)
                producto.costo_envio_por_kg = leer_numero("costo_envio_por_kg", float, 0)
            elif isinstance(producto, ProductoDigital):
                licencia = request.form["licencia"]
                if licencia not in ProductoDigital.MULTIPLICADORES:
                    raise ValueError("Selecciona un tipo de licencia válido.")
                producto.licencia = licencia
            elif isinstance(producto, ProductoPerecible):
                producto.dias_para_vencer = leer_numero("dias_para_vencer", int, 0)

            nueva_imagen = guardar_imagen(request.files.get("imagen"))
            if nueva_imagen:
                producto.imagen = nueva_imagen

            db.session.commit()
            flash(f"Producto '{producto.nombre}' actualizado correctamente.", "success")
            return redirect(url_for("detalle_producto", producto_id=producto.id))
        except ValueError as error:
            flash(str(error), "danger")
        except Exception:
            db.session.rollback()
            flash("Ocurrió un error al actualizar el producto.", "danger")

    return render_template("editar.html", producto=producto)


@app.route("/productos/<int:producto_id>/eliminar", methods=["POST"])
@login_requerido
@rol_requerido("admin")
def eliminar_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    producto.activo = False
    db.session.commit()
    flash(f"Producto '{producto.nombre}' desactivado del catálogo.", "success")
    return redirect(url_for("inicio"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "danger")
            return render_template("registro.html")

        if Usuario.query.filter_by(email=email).first():
            flash("Ya existe una cuenta con ese correo.", "danger")
            return render_template("registro.html")

        usuario = Usuario(nombre=nombre, email=email, rol="cliente")
        usuario.set_password(password)
        db.session.add(usuario)
        db.session.commit()

        flash("Cuenta creada correctamente. Ya puedes iniciar sesión.", "success")
        return redirect(url_for("login"))

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_password(password):
            session.clear()
            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre
            session["usuario_rol"] = usuario.rol
            session["carrito"] = {}
            flash(f"Bienvenido, {usuario.nombre}.", "success")
            return redirect(url_for("inicio"))

        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_requerido
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("inicio"))


@app.route("/carrito")
@login_requerido
def ver_carrito():
    lineas, total = construir_lineas_carrito()
    return render_template("carrito.html", lineas=lineas, total=total)


@app.route("/carrito/agregar/<int:producto_id>", methods=["POST"])
@login_requerido
def agregar_carrito(producto_id):
    producto = Producto.query.filter_by(id=producto_id, activo=True).first_or_404()
    cantidad = request.form.get("cantidad", 1, type=int)

    if cantidad is None or cantidad < 1:
        flash("La cantidad debe ser mayor que cero.", "danger")
        return redirect(url_for("detalle_producto", producto_id=producto.id))
    if producto.stock <= 0:
        flash("Este producto no tiene stock disponible.", "warning")
        return redirect(url_for("detalle_producto", producto_id=producto.id))

    carrito = obtener_carrito()
    clave = str(producto.id)
    nueva_cantidad = int(carrito.get(clave, 0)) + cantidad
    carrito[clave] = min(nueva_cantidad, producto.stock)
    session["carrito"] = carrito
    session.modified = True

    flash(f"'{producto.nombre}' fue agregado al carrito.", "success")
    return redirect(request.referrer or url_for("inicio"))


@app.route("/carrito/actualizar/<int:producto_id>", methods=["POST"])
@login_requerido
def actualizar_carrito(producto_id):
    producto = Producto.query.filter_by(id=producto_id, activo=True).first_or_404()
    cantidad = request.form.get("cantidad", type=int)

    if cantidad is None or cantidad < 1:
        flash("La cantidad debe ser al menos 1.", "danger")
        return redirect(url_for("ver_carrito"))

    carrito = obtener_carrito()
    carrito[str(producto_id)] = min(cantidad, producto.stock)
    session["carrito"] = carrito
    session.modified = True
    flash("Cantidad actualizada.", "success")
    return redirect(url_for("ver_carrito"))


@app.route("/carrito/eliminar/<int:producto_id>", methods=["POST"])
@login_requerido
def eliminar_del_carrito(producto_id):
    carrito = obtener_carrito()
    carrito.pop(str(producto_id), None)
    session["carrito"] = carrito
    session.modified = True
    flash("Producto eliminado del carrito.", "success")
    return redirect(url_for("ver_carrito"))


@app.route("/carrito/vaciar", methods=["POST"])
@login_requerido
def vaciar_carrito():
    session["carrito"] = {}
    session.modified = True
    flash("Carrito vaciado.", "success")
    return redirect(url_for("ver_carrito"))


@app.errorhandler(413)
def archivo_demasiado_grande(_error):
    flash("La imagen supera el límite de 5 MB.", "danger")
    return redirect(request.referrer or url_for("inicio"))


@app.errorhandler(404)
def pagina_no_encontrada(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
