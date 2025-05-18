import re
import filetype
from datetime import datetime

def select_camp(element):
    if element == '0':
        return "Campo obligatorio"
    else:
        return True
    
##función del aux
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
    return True


def validar_region(region):
    return select_camp(region)
def validar_comuna(comuna):
    return select_camp(comuna)
def validar_tamano(txt, min, max):
    if min <= len(txt) and len(txt)<= max:
        return True
    else:
        return False

###Validar nombre de la actividad
def validar_nombre(nombre):
    valid_length = validar_tamano(nombre, 4,200)
    return valid_length


##validar email
def validar_email(email):
    valid_length = validar_tamano(email,0,100)
    formato_valido= re.match(r'^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', email)
    return valid_length and bool(formato_valido)

##validar celular
def validar_celular(celular):
    if not celular:
        return True
    valid_length = validar_tamano(celular, 8, 15)
    print(valid_length)
    formato_valido = re.match(r"^\+\d{3}\.\d{8}$", celular)
    if formato_valido:
        return valid_length 
    else:
        return False


##Validar fechas
def validar_fecha_incio(date):
    if not date:
        return "La fecha y hora de inicio son requeridas."

    formato_esperado = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
    if not re.match(formato_esperado, date):
        return "El formato de la fecha y hora de inicio debe ser YYYY-MM-DDTHH:MM."
    else:
        return True

 
    
def validar_fecha_fin(inicio,fin):
    print(inicio)
    print(fin)
    if not fin:
        return True
    if fin is not None:
        formato_esperado = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
        if not re.match(formato_esperado, fin):
            return "El formato de la fecha y hora de término no es válido."


        
        elif not fin > inicio:
                    return "La fecha y hora de término deben ser posteriores a la fecha y hora de inicio."
        else:
                    return True 
            

    
##validar tema
def validar_tema(tema):
    return select_camp(tema)
    
##validar archivos
def validar_fotos(fotos):
    if not fotos:
        return True  

    if not (1 <= len(fotos) <= 5):
        return False

    for foto in fotos:
        if not validate_conf_img(foto):
            return False  

    return True

##Validar contactar por
def valida_contacto(contacto):
    if contacto is None:
        return True
    if contacto is not None:
        return True


##validar sector
def validar_sector(sector):
    if sector is None:
        return True
    else:
            if len(sector)>100:
                return "El largo máximo de sector es 100"
            else:
                return True
        



##Validar actividad
def validar_actividad(region,comuna, nombre, email, celular, sector, descripcion, inicio, fin, tema, contacto, fotos):
    print(f"Validando región: {region}")
    region_valida = validar_region(region)
    print(f"Resultado validación región: {region_valida}")

    print(f"Validando comuna: {comuna}")
    comuna_valida = validar_comuna(comuna)
    print(f"Resultado validación comuna: {comuna_valida}")

    print(f"Validando nombre: {nombre}")
    nombre_valido = validar_nombre(nombre)
    print(f"Resultado validación nombre: {nombre_valido}")

    print(f"Validando email: {email}")
    email_valido = validar_email(email)
    print(f"Resultado validación email: {email_valido}")

    print(f"Validando celular: {celular}")
    celular_valido = validar_celular(celular)
    print(f"Resultado validación celular: {celular_valido}")

    print(f"Validando sector: {sector}")
    sector_valido = validar_sector(sector)
    print(f"Resultado validación sector: {sector_valido}")

    print(f"Validando fecha inicio: {inicio}")
    fecha_incio_valida = validar_fecha_incio(inicio)
    print(f"Resultado validación fecha inicio: {fecha_incio_valida}")

    print(f"Validando fecha fin: {fin}")
    fecha_fin_valida = validar_fecha_fin(inicio, fin)
    print(f"Resultado validación fecha fin: {fecha_fin_valida}")

    print(f"Validando tema: {tema}")
    tema_valido = validar_tema(tema)
    print(f"Resultado validación tema: {tema_valido}")

    print(f"Validando contacto: {contacto}")
    contacto_valido = valida_contacto(contacto)
    print(f"Resultado validación contacto: {contacto_valido}")

    print(f"Validando fotos: {fotos}")
    fotos_validas = validar_fotos(fotos)
    print(f"Resultado validación fotos: {fotos_validas}")
    print()
    valida_todo = region_valida and comuna_valida and nombre_valido and email_valido and celular_valido and sector_valido and fecha_incio_valida and fecha_fin_valida and fotos_validas and tema_valido and contacto_valido
    if valida_todo:
        return True
    else:
        return False