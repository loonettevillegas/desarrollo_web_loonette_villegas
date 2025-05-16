from flask import Flask, request, render_template, redirect, url_for, session,jsonify
from utils.validations import validar_actividad
from database import db

from werkzeug.utils import secure_filename
import hashlib
import filetype
import os

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["GET"])
def index():
    ultimas_actividades = db.obtener_last_five_actividades()
    return render_template("auth/index.html", ultimas_actividades=ultimas_actividades)
#-----------------------------------------------------------------------------------
@app.route("/informar-actividad", methods = ["GET","POST"])
def informar_actividad():
    if request.method == "POST":
        error = ""
        region = request.form.get("region")
        comuna = request.form.get("comuna")
        nombre = request.form.get("Nombre organizador")
        email = request.form.get("email")
        celular = request.form.get("contacto")
        sector = request.form.get("areaTexto")
        contact = request.form.get("description-contact-input")
        theme = request.form.get("theme_input")
        inicio = request.form.get("date_inicio")
        fin = request.form.get("date_fin")
        fotos= request.form.get("fotos")
        descripcion = request.form.get("descripcioninput")
        if validar_actividad(region,comuna,nombre,email,celular,sector,descripcion,inicio,fin,theme, contact, fotos):
            ##si es válido registramos la actividad
            status, msg = db.create_actividad(region,comuna,nombre,email,celular,sector,descripcion,inicio,fin,theme, contact, fotos)

            error += msg
        else:
            error += "Uno de los campos no es valido."

        return render_template("auth/informar-actividad.html", error=error)

    elif request.method == "GET":
        region = request.args.get("region")
        temas = db.get_temas()
        medios_contactos = db.get_contactos()
        if region:
            comunas = db.get_comunas(region)
            comunas_data = [{"id": comuna.id, "nombre": comuna.nombre} for comuna in comunas]
            return jsonify(comunas_data)
        else:
            regiones = db.get_regions()
                
            return render_template("auth/informar-actividad.html",regiones=regiones, temas =temas, medios_contactos =medios_contactos)
    

@app.route("/listaActividades", methods = ["GET"])
def listaActividades():
    if request.method == "GET":
        
        return render_template("auth/listaActividades.html")##faltan 2 cosas revisar 
    
    
#----------------------------------------actividades----------------------------------------------
@app.route("/info-amigurumi", methods = ["GET"])
def info_amigurumi():
    return render_template("auth/info-amigurumi.html")

@app.route("/info-libros", methods = ["GET"])
def info_libros():
    return render_template("auth/info-libros.html")
@app.route("/info-mascota", methods = ["GET"])
def info_mascota():
    return render_template("auth/info-mascota.html")
@app.route("/info-origami", methods = ["GET"])
def info_origami():
    return render_template("auth/info-origami.html")

@app.route("/info-parque", methods = ["GET"])
def info_parque():
    return render_template("auth/info-parque.html")

@app.route("/estadisticas", methods = ["GET"])
def estadisticas():
    return render_template("auth/estadisticas.html")

#-------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)