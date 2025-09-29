from datetime import datetime
from flask import Flask, request, render_template, url_for, session, redirect, jsonify
from database.db import SessionLocal, Base, engine, AvisoAdopcion, Comuna, Region, Foto, ContactarPor
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
import uuid
import re
app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'cc5002',
    'password': 'programacionweb',
    'database': 'tarea2'
}
UPLOAD_FOLDER = os.path.join("static", "uploads").replace("\\", "/")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



@app.route("/api/regiones")
def api_regiones():
    session = SessionLocal()
    try:
        regiones = session.query(Region).all()
        data = []
        for r in regiones:
            data.append({
                "id": r.id,
                "nombre": r.nombre,
                "comunas": [{"id": c.id, "nombre": c.nombre} for c in r.comunas]
            })
        return jsonify(data)
    finally:
        session.close()

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)
@app.route("/")
def index():
    session = SessionLocal()
    try:
        avisos = (
            session.query(AvisoAdopcion)
            .options(
                joinedload(AvisoAdopcion.comuna),
                joinedload(AvisoAdopcion.fotos),
                joinedload(AvisoAdopcion.contactos)
            )
            .order_by(AvisoAdopcion.fecha_ingreso.desc())
            .limit(5)
            .all()
        )
    finally:
        session.close()

    return render_template("index.html", avisos=avisos)

@app.route("/listado")
def listado():
    session = SessionLocal()
    page = int(request.args.get("page", 1))
    per_page = 5

    avisos = (
        session.query(AvisoAdopcion)
        .options(
            joinedload(AvisoAdopcion.comuna),
            joinedload(AvisoAdopcion.fotos),       
            joinedload(AvisoAdopcion.contactos)   
        )
        .order_by(AvisoAdopcion.fecha_ingreso.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    total = session.query(AvisoAdopcion).count()
    session.close()
    return render_template("listado.html", avisos=avisos, page=page, total=total, per_page=per_page)

@app.route("/detalle/<int:aviso_id>")
def detalle(aviso_id):
    session = SessionLocal()
    try:
        aviso = (
            session.query(AvisoAdopcion)
            .options(
                joinedload(AvisoAdopcion.comuna),
                joinedload(AvisoAdopcion.fotos),
                joinedload(AvisoAdopcion.contactos)
            )
            .filter_by(id=aviso_id)
            .first()
        )
    finally:
        session.close()

    if not aviso:
        return "Aviso no encontrado", 404

    return render_template("detalle.html", aviso=aviso)


@app.route("/adopcion", methods=["GET", "POST"])
def crear_aviso():
    session = SessionLocal()

    if request.method == "POST":
        try:
            errores = []

            # --- Validaciones de campos ---
            nombre = request.form.get("nombre", "").strip()
            if not (3 <= len(nombre) <= 200):
                errores.append("El nombre debe tener entre 3 y 200 caracteres.")

            email = request.form.get("email", "").strip()
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) or len(email) > 100:
                errores.append("El correo no es válido o supera los 100 caracteres.")

            telefono = request.form.get("telefono", "").strip()
            if telefono and not re.match(r"^\+\d{3}\.\d{8}$", telefono):
                errores.append("El número debe tener formato +NNN.NNNNNNNN")

            cantidad = request.form.get("cantidad", "")
            if not cantidad.isdigit() or int(cantidad) < 1:
                errores.append("La cantidad debe ser un número entero mayor a 0.")

            edad = request.form.get("edad", "")
            if not edad.isdigit() or int(edad) < 1:
                errores.append("La edad debe ser un número entero mayor a 0.")

            unidad = request.form.get("unidadEdad")
            if unidad not in ["a", "m"]:
                errores.append("La unidad de edad debe ser 'a' (años) o 'm' (meses).")

            # Fecha
            fecha_entrega = None
            try:
                fecha_entrega = datetime.fromisoformat(request.form["fechaEntrega"])
                if fecha_entrega <= datetime.now():
                    errores.append("La fecha de entrega debe ser mayor a la actual.")
            except Exception:
                errores.append("Formato inválido en la fecha de entrega.")

            # ContactarPor
            for red in request.form.getlist("contactarPor"):
                identificador = request.form.get(f"contacto_{red}", "").strip()
                if not (4 <= len(identificador) <= 50):
                    errores.append(f"El contacto de {red} debe tener entre 4 y 50 caracteres.")

            # Fotos
            fotos = request.files.getlist("foto[]")
            for f in fotos:
                if f and f.filename:
                    if not allowed_file(f.filename):
                        errores.append(f"El archivo {f.filename} no tiene un formato permitido.")

            
            if errores:
                session.close()
                return render_template("adopcion.html", errores=errores)

            
            aviso = AvisoAdopcion(
                fecha_ingreso=datetime.now(),
                comuna_id=int(request.form["select-comuna"]),
                sector=request.form.get("sector"),
                nombre=nombre,
                email=email,
                celular=telefono if telefono else None,
                tipo=request.form["tipo"],
                cantidad=int(cantidad),
                edad=int(edad),
                unidad_medida=unidad,
                fecha_entrega=fecha_entrega,
                descripcion=request.form.get("descripcion"),
            )
            session.add(aviso)
            session.commit()

            # Guardar contactos
            for red in request.form.getlist("contactarPor"):
                identificador = request.form.get(f"contacto_{red}", "").strip()
                contacto = ContactarPor(nombre=red, identificador=identificador, aviso_id=aviso.id)
                session.add(contacto)
            
            # Guardar fotos
            for f in fotos:
                if f and f.filename and allowed_file(f.filename):
                    orig_filename = secure_filename(f.filename)
                    filename = f"{uuid.uuid4().hex}_{orig_filename}"

                    ruta = os.path.join(app.config["UPLOAD_FOLDER"], filename).replace("\\", "/")
                    f.save(ruta)

                    foto = Foto(
                        ruta_archivo=f"uploads/{filename}",
                        nombre_archivo=orig_filename,
                        aviso_id=aviso.id
                    )
                    session.add(foto)

            session.commit()
            session.close()
            return redirect(url_for("index"))

        except Exception as e:
            session.rollback()
            session.close()
            print("Error al guardar:", e)
            return render_template("adopcion.html", errores=[f"Error al guardar: {str(e)}"])
    
    session.close()
    return render_template("adopcion.html")
@app.route("/estadisticas")
def estadisticas():

    return render_template("estadisticas.html")

