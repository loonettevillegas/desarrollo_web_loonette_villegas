import re
import filetype
from datetime import datetime

def select_camp(element):
    if element == '0':
        return "Campo obligatorio"
def validate_conf_img(conf_img):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    # check if a file was submitted
    if conf_img is None:
        return False

    # check if the browser submitted an empty file
    if conf_img.filename == "":
        return False
    
    # check file extension
    ftype_guess = filetype.guess(conf_img)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

def validador_fotos(select_element, min, max):
    num_images = len(select_element)
    if not (min <= num_images <= max):
        return f"Debes seleccionar entre {max} y {min} fotos."
    return None


def validar_region(region):
    return select_camp(region)
def validar_comuna(comuna):
    return validar_comuna(comuna)
def validar_tamano(txt, min, max):
    if min <= len(txt) and len(txt)<= max:
        return "El campo debe tener entre {} y {} caracteres.".format(min, max)
    else:
        True

###Validar nombre de la actividad
def validar_nombre(nombre):
    valid_length = validar_tamano(nombre, 4,200)
    return valid_length


##validar email
def validar_email(email):
    valid_length = validar_tamano(email,0,100)
    formato_valido= re.match(r'^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', email)
    return valid_length and formato_valido

##validar celular
def validar_celular(celular):
    if not celular:
        return True
    valid_length = validar_tamano(celular, 8, 15)
    formato_valido = re.match(r'/^[0-9]+$/', celular)
    return valid_length and formato_valido


##Validar fechas
def validar_fecha_incio(date):
    if not date:
        return "La fecha y hora de inicio son requeridas."

    formato_esperado = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
    if not re.match(formato_esperado, date):
        return "El formato de la fecha y hora de inicio debe ser YYYY-MM-DDTHH:MM."

    try:
        date.fromisoformat(date.replace('T', ' '))
        return None  
    except ValueError:
        return "La fecha y hora de inicio no son válidas."
    
def validar_fecha_fin(inicio,fin):
    if not fin:
        return True
    if fin is not None:
        formato_esperado = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
        if not re.match(formato_esperado, fin):
            return "El formato de la fecha y hora de término debe ser YYYY-MM-DDTHH:MM."

        try:
            fecha_hora_termino = datetime.fromisoformat(fin.replace('T', ' '))
        except ValueError:
            return "La fecha y hora de término no son válidas."

        if inicio:
        
                fecha_hora_inicio = datetime.fromisoformat(inicio.replace('T', ' '))
                if not fecha_hora_termino > fecha_hora_inicio:
                    return "La fecha y hora de término deben ser posteriores a la fecha y hora de inicio."
            

    
##validar tema
def validar_tema(tema):
    return select_camp(tema)
    
##validar archivos
def validar_fotos(foto):
    return validador_fotos(foto, 1, 5) and validate_conf_img(foto)

##Validar contactar por
def valida_contacto(contacto):
    if contacto is None:
        return True
    if contacto is not None:
        largo_contacto = len(contacto)
        if largo_contacto >5:
            return "Puede seleccionar hasta 5 contactos"


##validar sector
def validar_sector(sector):
    if sector is None:
        return None
    if sector is not None:
        if len(sector)>100:
            return "El largo máximo de sector es 100"
        



##Validar actividad
def validar_actividad(region,comuna, nombre, email, celular, sector, descripcion, inicio, fin, tema, contacto, fotos):
    region_valida = validar_region(region)
    comuna_valida = validar_comuna(comuna)
    nombre_valido = validar_nombre(nombre)
    email_valido = validar_email(email)
    celular_valido = validar_celular(celular)
    sector_valido = validar_sector(sector)
    fecha_incio_valida = validar_fecha_incio(inicio)
    fecha_fin_valida = validar_fecha_fin(fin)
    tema_valido = validar_tema(tema)
    contacto_valido = valida_contacto(contacto)
    fotos_validas = validador_fotos(fotos)
    valida_todo = region_valida and comuna_valida and nombre_valido and email_valido and celular_valido and sector_valido and fecha_incio_valida and fecha_fin_valida and fotos_validas and tema_valido and contacto_valido
    return valida_todo