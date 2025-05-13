from flask import Flask, request, render_template, redirect, url_for, session
#from utils.validations import validate_login_user, validate_register_user, validate_confession
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
    return render_template("auth/index.html")
#-----------------------------------------------------------------------------------
@app.route("/informar-actividad", methods = ["GET","POST"])
def informar_actividad():
    if request.method == "POST":
        pass
    elif request.method == "GET":
        
        return render_template("auth/informar-actividad.html")
    

@app.route("/listaActividades", methods = ["GET","POST"])
def listaActividades():
    if request.method == "POST":
        pass
    elif request.method == "GET":
        
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