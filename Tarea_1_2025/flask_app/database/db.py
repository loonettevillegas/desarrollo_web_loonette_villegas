from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey,DateTime, Enum
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

#with open('database/querys.json', 'r') as querys:
#	QUERY_DICT = json.load(querys)

Base = declarative_base()



class Region(Base):
	__tablename__ = 'region'
	id =  Column(Integer, primary_key=True, autoincrement=True)
	nombre = Column(String(200), nullable=False)
	comunas = relationship("Comuna", backref="region")
	actividades = relationship("Actividad", backref="region")

class Comuna(Base):
    __tablename__ = 'comuna' 
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    region = relationship("Region", backref="comunas")


	


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
	id = Column(Integer, primary_key = True, autoincremente = True)
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



# -- conn ---

def get_conn():
	conn = pymysql.connect(
		db=DB_NAME,
		user=DB_USERNAME,
		passwd=DB_PASSWORD,
		host=DB_HOST,
		port=DB_PORT,
		charset=DB_CHARSET
	)
	return conn
with open('database/querys.json', 'r') as querys:
	QUERY_DICT = json.load(querys)
	
def get_regions():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute(QUERY_DICT["get_regiones"])
	regiones = cursor.fetchall()
	return regiones

def get_comunas():
	pass


def create_activity():
	pass