
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey,Enum, delete, func, case, and_, extract
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from werkzeug.utils import secure_filename
from flask import url_for
from sqlalchemy.orm import joinedload
from datetime import datetime

import os
import pymysql
import json
import enum

DB_NAME = "tarea2"
DB_USERNAME = "cc5002" 
DB_PASSWORD = "programacionweb" 
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"
UPLOAD_FOLDER = 'static/uploads'

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()



class Region(Base):
      __tablename__ = 'region'
      id =  Column(Integer, primary_key=True, autoincrement=True)
      nombre  = Column(String(200), nullable=False)
      #comunas = relationship("Comuna", backref="region")

class Comuna(Base):
    __tablename__ = 'comuna' 
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    region = relationship("Region", backref="comuna")


	


class Actividad(Base):
     __tablename__ = 'actividad'
     id = Column(Integer, primary_key=True, autoincrement=True)
     sector = Column(String(100), nullable=True)
     nombre = Column(String(200), nullable=False)
     email = Column(String(100), nullable=False)
     celular = Column(String(15), nullable=True)
     dia_hora_inicio = Column(DateTime, nullable=False)
     dia_hora_termino = Column(DateTime, nullable=True)
     descripcion = Column(String(500), nullable=True)
     comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False) 
     comuna = relationship("Comuna", backref="actividades")
     foto = relationship("Foto", back_populates="actividad")




class Foto(Base):
	__tablename__ =  'foto'
	id = Column(Integer, primary_key = True, autoincrement = True)
	ruta_archivo =  Column(String(300), nullable = False)
	nombre_archivo = Column(String(300), nullable = False)
	actividad_id = Column(Integer, ForeignKey('actividad.id'), primary_key=True)
	actividad = relationship("Actividad", backref="fotos")
	
class ContactarPorOpciones(enum.Enum):
    whatsapp = 'whatsapp'
    telegram = 'telegram'
    x = 'X'
    instagram = 'instagram'
    tiktok = 'tiktok'
    otra = 'otra'

class ContactarPor(Base):
    __tablename__ = 'contactar_por'  
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum(ContactarPorOpciones), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), primary_key=True) 
    actividad = relationship("Actividad", backref="contactos_por")

class Temas(enum.Enum):
	música = 'música'
	deporte = 'deporte'
	ciencias = 'ciencias'
	religión = 'religión'
	política = 'politica'
	tecnología = 'tecnología'
	juegos = 'juegos'
	baile = 'baile'
	comida = 'comida'
	otro = 'otro'

class ActividadTema(Base):
	__tablename__ =  'actividad_tema'
	id = Column(Integer, primary_key=True, autoincrement=True)
	tema = Column(Enum(Temas), nullable=False)
	glosa_otro = Column(String(15), nullable=True)
	actividad_id = Column(Integer, ForeignKey('actividad.id'), primary_key=True) 
	actividad = relationship("Actividad", backref="temas")

class Comentario(Base):
    __tablename__ =  'comentario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(80), nullable=False)
    texto = Column(String(300), nullable=False)
    fecha = Column(DateTime, nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)
    actividad = relationship("Actividad", backref="comentarios")



    
    

     


# -- definir funciones ---


	
def get_regions():
    session = SessionLocal()
    try:
        regions = session.query(Region).all()
        return regions
    finally:
        session.close()

def get_comunas(region_id):
	session = SessionLocal()
	try:
		comunas = session.query(Comuna).filter_by(region_id=region_id).all()
		return comunas
	finally:
		session.close()


def create_actividad(region,comuna,nombre,email,celular,sector,descripcion,inicio,fin,theme, contact,contact_description, fotos):
    session = SessionLocal()
    
    nueva_actividad = Actividad(
            sector=sector,
            nombre=nombre,
            email=email,
            celular=celular,
            dia_hora_inicio=inicio,
            dia_hora_termino=fin,
            descripcion=descripcion,
            comuna_id=comuna
        )
    session.add(nueva_actividad)
    session.flush() 

    
    create_temas(session, nueva_actividad.id, theme)
    create_fotos(session, nueva_actividad.id, fotos)


    if contact:
            create_contacto(session, nueva_actividad.id, contact,contact_description)

    

    session.commit()
    session.close()

    return True 
    

def create_temas(session, actividad_id, temas):
    if isinstance(temas, list):
        for tema_str in temas:
            try:
                tema_enum_value = Temas(tema_str)  
                actividad_tema = ActividadTema(actividad_id=actividad_id, tema=tema_enum_value)
                session.add(actividad_tema)
            except ValueError:
                print(f"Error: El valor '{tema_str}' no es un tema válido.")
    elif isinstance(temas, str):
        try:
            tema_enum_value = Temas(temas)
            actividad_tema = ActividadTema(actividad_id=actividad_id, tema=tema_enum_value)
            session.add(actividad_tema)
        except ValueError:
            print(f"Error: El valor '{temas}' no es un tema válido.")

def create_contacto(session, actividad_id, contactos,contact_description):
    for contacto in contactos:
            try:
                
                nombre_contacto = ContactarPorOpciones(contacto) 
                identificador_contacto = contact_description    
                contacto = ContactarPor(
                    actividad_id=actividad_id,
                    nombre=nombre_contacto,
                    identificador=identificador_contacto
                )
                session.add(contacto)
            except ValueError as e:
                print(f"Error al crear contacto: {e}")
def create_fotos(session, actividad_id, fotos):
    for foto in fotos:
        if foto:
            filename = secure_filename(foto.filename)
            ruta_destino_completa = os.path.join(UPLOAD_FOLDER, filename)
            ruta_archivo_db = os.path.join('uploads', filename).replace('\\', '/') 
            nombre_archivo_db = filename
            try:
                foto.save(ruta_destino_completa)
                nuevo_archivo = Foto(
                    actividad_id=actividad_id,
                    ruta_archivo=ruta_archivo_db,
                    nombre_archivo=nombre_archivo_db
                )
                session.add(nuevo_archivo)
            except Exception as e:
                print(f"Error al guardar el archivo: {e}")
                session.rollback()

def create_comentario(new_nombre, new_comentario,id_actividad):
    session = SessionLocal()
    nuevo_comentario = Comentario(nombre= new_nombre, texto = new_comentario,fecha=datetime.now(),    
            actividad_id=id_actividad)
    session.add(nuevo_comentario)

    session.commit()
    session.close()
    return True
    
def obtener_comentarios(id):
     session = SessionLocal()

     comentarios = session.query(Comentario).filter_by(actividad_id=id)
     
     session.close()
     return comentarios
     
def obtener_last_five_actividades():
    session = SessionLocal()
    try:
        ultimas_actividades = session.query(Actividad) \
                                       .order_by(Actividad.id.desc()) \
                                       .limit(5) \
                                       .options(joinedload(Actividad.foto)) \
                                       .all()
        return ultimas_actividades
    finally:
        session.close()
        
def obtener_tema_por_id(actividad_id):
     session = SessionLocal()
     actividad_tema = session.query(ActividadTema).filter_by(actividad_id=actividad_id).first()
     session.close()
     return actividad_tema.tema.value if actividad_tema else None


def comuna_por_id(id):
    session = SessionLocal()
    try:
        comuna = session.query(Comuna).filter(Comuna.id == id).first()
        return comuna.nombre if comuna else None
    finally:
        session.close()
def foto_por_id(id):
    session = SessionLocal()
    try:
        foto_ruta_relativa = session.query(Foto.ruta_archivo).filter(Foto.actividad_id == id).first()
        if foto_ruta_relativa:
            ruta_completa = url_for('static', filename=foto_ruta_relativa[0])
            print(f"Ruta de la foto encontrada para actividad {id}: {ruta_completa}")
            return ruta_completa
        else:
            print(f"No se encontró foto para actividad {id}")
            return None
    finally:
        session.close()
def obtener_todas_actividades(page):
    session = SessionLocal()
    try:
        offset = (page - 1) * 5
        actividades = session.query(Actividad).limit(5).offset(offset).all()
        return actividades
    finally:
        session.close()    
def cantidad_actividades():
     session = SessionLocal()
     sum = session.query(Actividad).count()
    
     session.close()

     return sum
def obtener_actividad_por_id(id):
    session = SessionLocal()
    actividad = session.query(Actividad).filter(Actividad.id == id).first()
    
    session.close()
    return actividad


def obtener_actividades_por_tipo():
     session =  SessionLocal()
     actividades_por_tipo =  session.query(
            ActividadTema.tema,
            func.count(ActividadTema.id).label('count')
        ).group_by(
            ActividadTema.tema
        ).all()
     session.close()

     return [{'type': row.tema.value, 'count': row.count} for row in actividades_por_tipo]


def obtener_actividades_por_meses_y_horas():
    session = SessionLocal()
    meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
    hora  = extract('hour', Actividad.dia_hora_inicio)
    mañana = and_(hora >= 8, hora <= 11)
    mediodia = and_(hora >= 12, hora <= 17)
    tarde = and_(hora >= 18, hora <= 23)
    actividades_segun_hora = session.query(
            extract('year', Actividad.dia_hora_inicio).label('year_num'),
            extract('month', Actividad.dia_hora_inicio).label('month_num'),
            func.sum(case((mañana, 1), else_=0)).label('cantidad_en_mañana'),
            func.sum(case((mediodia, 1), else_=0)).label('cantidad_en_mediodia'),
            func.sum(case((tarde, 1), else_=0)).label('cantidad_en_tarde')
        ).group_by(
            extract('year', Actividad.dia_hora_inicio),
            extract('month', Actividad.dia_hora_inicio)
        ).order_by(
            extract('year', Actividad.dia_hora_inicio),
            extract('month', Actividad.dia_hora_inicio)
        ).all()
    datos_por_mes = []
    for row in actividades_segun_hora:
            month_label = f"{meses.get(row.month_num, 'Desconocido')} {row.year_num}"
            datos_por_mes.append({
                'month_label': month_label,
                'mañana': int(row.cantidad_en_mañana),
                'mediodia': int(row.cantidad_en_mediodia),
                'tarde': int(row.cantidad_en_tarde)
            })
    session.close()
    return datos_por_mes


     


def foto_detalle(id):
    session = SessionLocal()
    
    fotos = session.query(Foto.ruta_archivo).filter(Foto.actividad_id == id).all()
    rutas_corregidas = []
    for foto in fotos:
        if foto and foto[0]:
                ruta_corregida = foto[0].replace('\\', '/')
                rutas_corregidas.append(ruta_corregida)
    
    session.close()

    return rutas_corregidas
    

def obtener_contacto_por_id(id):
     session = SessionLocal()
     contacto = session.query(ContactarPor).filter(ContactarPor.actividad_id == id).first()
     session.close()
     return contacto

def obtener_actividades_por_dia():
     session= SessionLocal()
     actividades_por_dia = session.query(
            func.date(Actividad.dia_hora_inicio).label('Fecha'),
            func.count(Actividad.id).label('conteo')
        ).group_by(
            func.date(Actividad.dia_hora_inicio)
        ).order_by(
            func.date(Actividad.dia_hora_inicio) 
        ).all()

        

     session.close()
     return [{'date': str(row.Fecha), 'count': row.conteo} for row in actividades_por_dia] 
def eliminar_todos_los_datos(nombre_tabla):
    session = SessionLocal()
    try:
        if nombre_tabla == "actividad":
            modelo = Actividad
        elif nombre_tabla == "foto":
            modelo = Foto
        elif nombre_tabla == "contactar_por":
            modelo = ContactarPor
        elif nombre_tabla == "actividad_tema":
            modelo = ActividadTema
        else:
            print(f"Tabla '{nombre_tabla}' no reconocida.")
            return

        stmt = delete(modelo)
        result = session.execute(stmt)
        session.commit()
        print(f"Se eliminaron {result.rowcount} registros de la tabla '{nombre_tabla}'.")
    except Exception as e:
        session.rollback()
        print(f"Error al eliminar datos de la tabla '{nombre_tabla}': {e}")
    finally:
        session.close()

#eliminar_todos_los_datos('foto')
##eliminar_todos_los_datos('actividad_tema')
##eliminar_todos_los_datos('contactar_por')
##eliminar_todos_los_datos('actividad')

