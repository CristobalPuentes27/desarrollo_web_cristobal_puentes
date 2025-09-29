from datetime import datetime
from flask import Flask, request, render_template, url_for, session, redirect, jsonify
from database.db import SessionLocal, Base, engine, AvisoAdopcion, Comuna, Region, Foto, ContactarPor
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
from markupsafe import escape
import uuid
app = Flask(__name__)

# Configura conexión a MySQL (ajusta usuario, clave y base)
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
    per_page = 10

    avisos = (
        session.query(AvisoAdopcion)
        .options(
            joinedload(AvisoAdopcion.comuna),
            joinedload(AvisoAdopcion.fotos),       # 👈 cargamos fotos
            joinedload(AvisoAdopcion.contactos)    # 👈 y contactos, si los muestras
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
            # Datos principales
            aviso = AvisoAdopcion(
                fecha_ingreso=datetime.now(),
                comuna_id=int(request.form["select-comuna"]),
                sector=request.form.get("sector"),
                nombre=request.form["nombre"],
                email=request.form["email"],
                celular=request.form.get("telefono"),
                tipo=request.form["tipo"],
                cantidad=int(request.form["cantidad"]),
                edad=int(request.form["edad"]),
                unidad_medida=request.form["unidadEdad"],
                fecha_entrega=datetime.fromisoformat(request.form["fechaEntrega"]),
                descripcion=request.form.get("descripcion")
            )
            session.add(aviso)
            session.commit()

            # Redes sociales seleccionadas
            for red in request.form.getlist("contactarPor"):  # 👈 ahora sí llegan
                identificador = request.form.get(f"contacto_{red}", "").strip()
                if identificador:
                    contacto = ContactarPor(
                        nombre=red,
                        identificador=identificador,
                        aviso_id=aviso.id
                    )
                    session.add(contacto)
            # Fotos
            fotos = request.files.getlist("foto[]")
            for f in fotos:
                if f and f.filename and allowed_file(f.filename):
                    orig_filename = secure_filename(f.filename)
                    filename = f"{uuid.uuid4().hex}_{orig_filename}"  # ej: "8f3e2c7a_gatito.jpg"

                    # Ruta donde se guardará el archivo
                    ruta = os.path.join(app.config["UPLOAD_FOLDER"], filename).replace("\\", "/")
                    f.save(ruta)

                    # Guardamos solo la ruta **relativa a static**
                    foto = Foto(
                        ruta_archivo=f"uploads/{filename}",  # esto va a la DB
                        nombre_archivo=orig_filename,        # nombre original
                        aviso_id=aviso.id
                    )
                    session.add(foto)

            session.commit()
            return redirect(url_for("listado"))

        except Exception as e:
            session.rollback()
            print("Error al guardar:", e)
    session.close()
    return render_template("adopcion.html")
@app.route("/estadisticas")
def estadisticas():

    return render_template("estadisticas.html")
if __name__ == '__main__':
    app.run(debug=True)
