
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey,Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

import pymysql
import json
import enum

DB_NAME = "tarea2"
DB_USERNAME = "cc5002" 
DB_PASSWORD = "programacionweb" 
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

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
	musica = 'música'
	deporte = 'deporte'
	ciencias = 'ciencias'
	religion = 'religión'
	politica = 'política'
	tecnologia = 'tecnología'
	juegos = 'juegos'
	baile = 'baile'
	comida = 'comida'
	otro = 'otro'

class ActividadTema(Base):
	__tablename__ =  'actividad_tema'
	id = Column(Integer, primary_key=True, autoincrement=True)
	tema = Column(Enum(Temas), nullable=False)
	glosa_otro = Column(String(15), nullable=True)
	actividad_id = Column(Integer, ForeignKey('actividad.id'), primary_key=True) # Clave primaria compuesta
	actividad = relationship("Actividad", backref="temas")



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


def create_actividad(sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion, region_id, comuna_id, temas_ids, contactos_ids, nombres_archivos):
    session = SessionLocal()
    try:
        nueva_actividad = Actividad(
            sector=sector,
            nombre=nombre,
            email=email,
            celular=celular,
            dia_hora_inicio=dia_hora_inicio,
            dia_hora_termino=dia_hora_termino,
            descripcion=descripcion,
            region_id=region_id,
            comuna_id=comuna_id
        )
        session.add(nueva_actividad)
        session.flush() 

        if temas_ids:
            save_actividad_temas(session, nueva_actividad.id, temas_ids)


        if contactos_ids:
            save_actividad_contactos(session, nueva_actividad.id, contactos_ids)

        if nombres_archivos:
            save_actividad_archivos(session, nueva_actividad.id, nombres_archivos)

        session.commit()
        return True, nueva_actividad.id 
    except Exception as e:
        session.rollback()
        return False, str(e) 
    finally:
        session.close()

def save_actividad_temas(session, actividad_id, temas_ids):
    for tema_id in temas_ids:
        actividad_tema = ActividadTema(actividad_id=actividad_id, tema_id=tema_id)
        session.add(actividad_tema)

def save_actividad_contactos(session, actividad_id, contactos_ids):
    for contacto_id in contactos_ids:
        contacto = ContactarPor(actividad_id=actividad_id, medio_contacto_id=contacto_id)
        session.add(contacto)

def save_actividad_archivos(session, actividad_id, nombres_archivos):
    for nombre_archivo in nombres_archivos:
        archivo = Foto(actividad_id=actividad_id, nombre_archivo=nombre_archivo)
        session.add(archivo)
def obtener_last_five_actividades():
    session = SessionLocal()
    try:
        ultimas_actividades = session.query(Actividad) \
                                       .order_by(Actividad.id.desc()) \
                                       .limit(5) \
                                       .all()
        return ultimas_actividades
    finally:
        session.close()
        
def get_temas():
    session = SessionLocal()
    themes = session.query(ActividadTema).all()
    session.close()

    return themes
def get_contactos():
    session = SessionLocal()
    medios_contactos = session.query(ContactarPor).all()
    session.close()

    return medios_contactos
    