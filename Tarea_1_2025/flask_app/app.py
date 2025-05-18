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
    return render_template("auth/index.html", ultimas_actividades=ultimas_actividades,obtener_tema=db.obtener_tema_por_id, obtener_comuna= db.comuna_por_id, obtener_foto= db.foto_por_id)
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
        contact = request.form.getlist("contact_se")
        contact_description = request.form.get("description-contact-input")
        theme = request.form.get("theme_input")
        inicio = request.form.get("date_inicio")
        fin = request.form.get("date_fin")
        fotos= request.files.getlist("fotos")
        descripcion = request.form.get("descripcioninput")

        valid_activity= validar_actividad(region,comuna,nombre,email,celular,sector,descripcion,inicio,fin,theme, contact, fotos)
        print(valid_activity)
        if valid_activity:
            activity = db.create_actividad(region,comuna,nombre,email,celular,sector,descripcion,inicio,fin,theme, contact,contact_description, fotos)

            
            if activity is None:
                        return jsonify({'success': False,  "message": " No se pudo"})

           

        
        return jsonify({'success': True,  "message": " Se pudo"})




    elif request.method == "GET":
        region = request.args.get("region")
        temas = db.Temas
        medios_contactos = db.ContactarPorOpciones
        
        if region:
            comunas = db.get_comunas(region)
            comunas_data = [{"id": comuna.id, "nombre": comuna.nombre} for comuna in comunas]
            return jsonify(comunas_data)
        else:
            regiones = db.get_regions()
            print(medios_contactos)
            return render_template("auth/informar-actividad.html",regiones=regiones, temas =temas, medios_contactos = medios_contactos)
    

@app.route("/listaActividades", methods = ["GET"])
def listaActividades():
    if request.method == "GET":
        page = request.args.get('page', 1, type=int)
        actividades =db.obtener_todas_actividades(page)
        paginas = (db.cantidad_actividades()+5-1)//5
        print(f"NUMERO DE PÁGINAS",paginas)
        print(f"NUMERO DE actividades",actividades)
        tabla=[]
        for actividad in actividades:
            tema =db.obtener_tema_por_id(actividad.id)
            comuna = db.comuna_por_id(actividad.comuna_id)
            fotos= db.foto_por_id(actividad.id)
            
            tabla.append({
                'Inicio':actividad.dia_hora_inicio,
                'Termino': actividad.dia_hora_termino,
                'Comuna': comuna,
                'Sector': actividad.sector,
                'Tema': tema,
                'Nombre organizador': actividad.nombre,
                'Total fotos': fotos,
                'id' : actividad.id
                
                
                })
        
        return render_template('auth/listaActividades.html', actividades=tabla, total_pages=paginas, current_page=page)

@app.route("/actividades_paginadas", methods=["GET"])
def actividades_paginadas():
    page = request.args.get('page', 1, type=int)
    actividades =db.obtener_todas_actividades(page)
    paginas = (db.cantidad_actividades()+5-1)//5
    print(f"NUMERO DE PÁGINAS",paginas)
    print(f"NUMERO DE actividades",actividades)
    tabla=[]
    for actividad in actividades:
            tema =db.obtener_tema_por_id(actividad.id)
            comuna = db.comuna_por_id(actividad.comuna_id)
            fotos= db.foto_por_id(actividad.id)
            tabla.append({
                'Inicio':actividad.dia_hora_inicio,
                'Termino': actividad.dia_hora_termino,
                'Comuna': comuna,
                'Sector': actividad.sector,
                'Tema': tema,
                'Nombre organizador': actividad.nombre,
                'Total fotos': fotos,
                'id' : actividad.id
                
                
                })

    total_actividades = db.cantidad_actividades()
    total_pages = (total_actividades + 5 - 1) // 5

    return jsonify({
        'actividades': tabla,
        'total_pages': total_pages,
        'current_page': page
    })
    
#----------------------------------------actividades----------------------------------------------
@app.route("/detalle/<int:id>", methods=["GET"])
def detalle(id):
    print(id)
    actividad = db.obtener_actividad_por_id(id)
    print(f'esta',actividad.id)
    return render_template("auth/detalle.html", actividad = actividad, obtener_tema=db.obtener_tema_por_id, obtener_comuna= db.comuna_por_id, obtener_foto= db.foto_detalle, obtener_contacto = db.obtener_contacto_por_id)

@app.route("/estadisticas", methods = ["GET"])
def estadisticas():
    return render_template("auth/estadisticas.html")

#-------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)