from datetime import datetime
from flask import Flask, request, render_template, url_for, session, redirect, jsonify
from database.db import SessionLocal, Base, engine, AvisoAdopcion, Comuna, Region, Foto, ContactarPor, Comentario
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
from collections import defaultdict
import hashlib
import filetype
import os
import uuid
import re
import random
from datetime import timedelta
from faker import Faker

fake = Faker('es_CL')
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
            if len(fotos) == 0 or all(f.filename == "" for f in fotos):
                errores.append("Debe subir al menos una foto.")
            if len(fotos) > 5:
                errores.append("No puede subir más de 5 fotos.")
            
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
@app.route("/api/estadisticas")
def api_estadisticas():
    session = SessionLocal()
    try:
        # Obtener todos los registros reales
        rows = session.query(AvisoAdopcion.fecha_ingreso, AvisoAdopcion.tipo).all()
        print(f"Registros reales encontrados: {len(rows)}")

        fecha_mas_antigua = None
        for fecha_ingreso, tipo in rows:
            if fecha_ingreso:
                
                if isinstance(fecha_ingreso, datetime):
                    fecha_date = fecha_ingreso.date()
                else:
                    # Por si acaso, pero debería ser datetime
                    fecha_date = fecha_ingreso.date()
                
                if fecha_mas_antigua is None or fecha_date < fecha_mas_antigua:
                    fecha_mas_antigua = fecha_date

        # Si no hay fechas en la BD, usar fecha por defecto (hace 30 días)
        if fecha_mas_antigua is None:
            fecha_mas_antigua = datetime.now().date() - timedelta(days=30)
            print(f"No se encontraron fechas, usando por defecto: {fecha_mas_antigua}")
        else:
            print(f"Fecha más antigua en BD: {fecha_mas_antigua}")

        # Generar datos fake para fechas ANTERIORES a la fecha más antigua
        if len(rows) < 100:
            # Generar datos de los últimos 180 días antes de la fecha más antigua
            dias_para_atras = 180
            fecha_inicio_fake = fecha_mas_antigua - timedelta(days=dias_para_atras)
            
            cantidad_fake = 100 - len(rows)
            fake_data = generar_datos_fake_para_estadisticas(
                n=cantidad_fake, 
                fecha_inicio=fecha_inicio_fake, 
                fecha_fin=fecha_mas_antigua
            )
            rows += fake_data
            print(f"Se agregaron {len(fake_data)} datos falsos desde {fecha_inicio_fake} hasta {fecha_mas_antigua}")

        # Procesar datos (real + fake)
        by_day = defaultdict(int)
        by_type = defaultdict(int)
        by_month_type = defaultdict(lambda: defaultdict(int))

        for fecha_ingreso, tipo in rows:
            if not fecha_ingreso:
                continue

            
            if isinstance(fecha_ingreso, datetime):
                dt = fecha_ingreso.date()
            else:
                dt = fecha_ingreso.date()

            day_key = dt.isoformat()
            month_key = dt.strftime("%Y-%m")

            by_day[day_key] += 1
            by_type[tipo] += 1
            by_month_type[month_key][tipo] += 1

        sorted_days = sorted(by_day.items(), key=lambda x: x[0])
        days_list = [{"date": d, "count": c} for d, c in sorted_days]

        pie = {"gato": int(by_type.get("gato", 0)), "perro": int(by_type.get("perro", 0))}

        months = sorted(by_month_type.keys())
        gatos_arr = [int(by_month_type[m].get("gato", 0)) for m in months]
        perros_arr = [int(by_month_type[m].get("perro", 0)) for m in months]

        result = {
            "by_day": days_list,
            "by_type": pie,
            "by_month": {
                "months": months,
                "gatos": gatos_arr,
                "perros": perros_arr
            }
        }

        print(f"Datos procesados: {len(days_list)} días, {pie} tipos, {len(months)} meses")
        return jsonify(result)
        
    except Exception as e:
        print(f"Error en api_estadisticas: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500
    finally:
        session.close()

def generar_datos_fake_para_estadisticas(n=120, fecha_inicio=None, fecha_fin=None):
    """
    Genera n registros falsos de avisos para usar en los gráficos (no se guardan).
    Genera datos entre fecha_inicio y fecha_fin (exclusivo de fecha_fin).
    """
    data = []
    tipos = ["gato", "perro"]
    
    
    if fecha_inicio is None:
        fecha_inicio = datetime.now().date() - timedelta(days=180)
    if fecha_fin is None:
        fecha_fin = datetime.now().date()
    
    
    dias_rango = (fecha_fin - fecha_inicio).days
    if dias_rango <= 0:
        dias_rango = 180
        fecha_inicio = fecha_fin - timedelta(days=dias_rango)
    
    print(f"Generando {n} datos fake desde {fecha_inicio} hasta {fecha_fin}")
    
    for _ in range(n):

        dias_aleatorios = random.randint(0, dias_rango - 1)
        fecha_fake = fecha_inicio + timedelta(days=dias_aleatorios)
        
        
        fecha_fake_dt = datetime.combine(fecha_fake, datetime.min.time())
        tipo = random.choice(tipos)
        data.append((fecha_fake_dt, tipo))
    
    return data

@app.route("/estadisticas") 
def estadisticas(): 
    return render_template("estadisticas.html")

@app.route("/aviso/<int:aviso_id>/comentarios")
def obtener_comentarios(aviso_id):
    session = SessionLocal()
    try:
        aviso = session.query(AvisoAdopcion).get(aviso_id)
        if not aviso:
            return jsonify([])
        
        comentarios = []
        for comentario in aviso.comentarios:
            comentarios.append({
                'id': comentario.id,
                'nombre': comentario.nombre,
                'texto': comentario.texto,
                'fecha': comentario.fecha.strftime('%d/%m/%Y %H:%M')
            })
        
        return jsonify(comentarios)
    finally:
        session.close()
import re
from html import escape

@app.route("/aviso/<int:aviso_id>/comentario", methods=["POST"])
def agregar_comentario(aviso_id):
    session = SessionLocal()
    try:
        # Verificar que el aviso existe
        aviso = session.query(AvisoAdopcion).get(aviso_id)
        if not aviso:
            return jsonify({'success': False, 'errores': ['Aviso no encontrado']}), 404
        
        # Verificar Content-Type
        if not request.is_json:
            return jsonify({'success': False, 'errores': ['Content-Type debe ser application/json']}), 400
        
        # Obtener datos
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'errores': ['Datos JSON inválidos']}), 400
            
        nombre = data.get('nombre', '').strip()
        texto = data.get('texto', '').strip()
        
        
        errores = []
        
        
        if len(nombre) < 3 or len(nombre) > 80:
            errores.append('El nombre debe tener entre 3 y 80 caracteres')
        
        if len(texto) < 5:
            errores.append('El comentario debe tener al menos 5 caracteres')
        
        
        if not re.match(r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\-\'\.\,\(\)]{3,80}$', nombre):
            errores.append('El nombre contiene caracteres no permitidos')
        
        
        if nombre.replace(' ', '').replace('\t', '') == '':
            errores.append('El nombre no puede estar vacío')
        
        if texto.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', '') == '':
            errores.append('El comentario no puede estar vacío')
        
        
        patrones_maliciosos = [
            r'<script.*?>.*?</script>',  # Etiquetas script
            r'javascript:',              # Protocolo javascript
            r'on\w+\s*=',               # Event handlers (onclick, onload, etc.)
            r'<iframe.*?>.*?</iframe>',  # Iframes
            r'<object.*?>.*?</object>',  # Objects
            r'<embed.*?>.*?</embed>',    # Embeds
            r'<form.*?>.*?</form>',      # Forms
            r'expression\s*\(',          # CSS expressions
            r'vbscript:',                # VBScript
            r'<meta.*?>',                # Meta tags
            r'<link.*?>',                # Link tags
            r'<style.*?>.*?</style>',    # Style tags
        ]
        
        for patron in patrones_maliciosos:
            if re.search(patron, nombre, re.IGNORECASE | re.DOTALL):
                errores.append('El nombre contiene código no permitido')
                break
            if re.search(patron, texto, re.IGNORECASE | re.DOTALL):
                errores.append('El comentario contiene código no permitido')
                break
        
        if len(nombre) > 80:
            errores.append('El nombre es demasiado largo')
        if len(texto) > 1000:  # Más generoso que el límite de la DB
            errores.append('El comentario es demasiado largo')
        
        if errores:
            return jsonify({'success': False, 'errores': errores}), 400
        
       
        nombre_seguro = escape(nombre)
        texto_seguro = escape(texto)
        
        
        nombre_seguro = re.sub(r'\s+', ' ', nombre_seguro.strip())
        texto_seguro = re.sub(r'\n\s*\n', '\n\n', texto_seguro.strip())
        
        # Crear comentario con datos sanitizados
        nuevo_comentario = Comentario(
            nombre=nombre_seguro,
            texto=texto_seguro,
            aviso_id=aviso_id
        )
        
        session.add(nuevo_comentario)
        session.commit()
        
        return jsonify({
            'success': True,
            'comentario': {
                'id': nuevo_comentario.id,
                'nombre': nuevo_comentario.nombre,  # Ya sanitizado
                'texto': nuevo_comentario.texto,    # Ya sanitizado
                'fecha': nuevo_comentario.fecha.strftime('%d/%m/%Y %H:%M')
            }
        })
        
    except Exception as e:
        session.rollback()
        print(f"Error al guardar comentario: {str(e)}")
        # No revelar detalles del error al cliente
        return jsonify({'success': False, 'errores': ['Error interno del servidor']}), 500
    finally:
        session.close()