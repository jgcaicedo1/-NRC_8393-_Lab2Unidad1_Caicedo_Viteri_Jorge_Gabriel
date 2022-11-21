"""
    UNIVERSIDAD DE LAS FUERZAS ARMADAS ESPE
                
                LABORATORIO No1

        Autor:Jorge Gabriel Caicedo Viteri

        Materia:Sistema de Base de Datos

                   2022-2023

"""
#Librerias de nuestro laboratorio
import pandas as pd
import uuid
import random
from faker import Faker
import datetime

#Total de registros a generar
num_usuarios = 5000
"""
Definicion de los atributos de la entidad Estudiante

ID(id)=El id del estudiante que sera unico para cada uno
Nombre(nombre)=El nombre del estudiante generado aleatoriamente.
Apellido(apellido)=El apellido del estudiante generado aleatoriamente.
Genero(genero)=El genero del estudiante que sera masculino o femenino.
Nivel Academico(nivel_academico)=En niños parvulos solo existen 1 nivel y 2 nivel.
Edad(edad)=La edad del estudiante que ira solo entre 2-5 años.
Fecha de Nacimiento(fecha_de_nacimiento)=La fecha de nacimiento del estudiante.
Email(email)=Un email que funcionara solo como identificacion del estudiante para el docente.
Foto(foto)=Una foto del estudiante que lo ayudara para ingresar en el sistema.

"""

caracteristicas = [
    "id" ,
    "nombre" ,
    "apellido" ,
    "genero" ,
    "nivel_academico",
    "edad" ,
    "fecha_de_nacimiento" ,
    "email" ,
    "foto"
    ]
#Elaboración del dataframe
df = pd.DataFrame(columns=caracteristicas)
#Generacion aleatoria del id del estudiante
df['id'] = [uuid.uuid4().hex for i in range(num_usuarios)]

#Generacion aleatoria del genero del estudiante
generos = ["Masculino", "Femenino"]

df['genero'] = random.choices(
    generos,
    weights=(60,40),
    k=num_usuarios
    )

#Libreria que usaremos para generar los nombres aleatorios
faker = Faker('es_CO')

def nombre_gen(genero):
    """
    Funcion para generar nombres aleatorios de acuerdo al genero.

    Parametros
    ----------

        genero : str
            
            Variable tipo String del genero que espera  la función.

    Retorna
    -------

        Retornara el nombre dependiendo si es masculino o femenino

    """

    if genero=='Masculino':
        return faker.first_name_male()
    elif genero=='Femenino':
        return faker.first_name_female()

#Generacion Aleatoria del nombre del estudiante
df['nombre'] = [nombre_gen(i) for i in df['genero']]
#Generacion Aleatoria del apellido del estudiante
df['apellido'] = [faker.last_name() for i in df['genero']]

def emailGen(nombre,apellido,duplicateFound=False):
    """
    Funcion para generar emails aleatorios de acuerdo al nombre y apellido del estudiante.

    Parametros
    ----------

        nombre : str
            
            Variable tipo String del nombre del estudiante que espera  la función.

        apellido : str
            
            Variable tipo String del apellido del estudiante que espera  la función.

        duplicateFound : bool
            
            Variable tipo Bool que funcionara para identificar duplicados.

    Retorna
    -------

        Retornara el email del estudiante de acuerdo a sus datos.

    """
    dom = "@educacion.edu.ec" #Dominio de la institucion academica
    nombre = nombre.lower().split(" ")
    apellido = apellido.lower().split(" ")
    chars = [".","_"]
    nuevo_nombre = nombre[0] + random.choice(chars) + apellido[0]
    
    if duplicateFound:#En caso de encontrar duplicados
        num = random.randint(0,100)
        nuevo_nombre = nuevo_nombre + str(num)
    
    return nuevo_nombre + dom

def fotoGen(nombre,apellido,duplicateFound=False):
    """
    Funcion para generar urls aleatorios de la foto del estudiante de acuerdo al nombre y apellido del estudiante.

    Parametros
    ----------

        nombre : str
            
            Variable tipo String del nombre del estudiante que espera  la función.

        apellido : str
            
            Variable tipo String del apellido del estudiante que espera  la función.

        duplicateFound : bool
            
            Variable tipo Bool que funcionara para identificar duplicados.

    Retorna
    -------

        Retornara el url de la foto del estudiante de acuerdo a sus datos.

    """
    url ="https://www.mcb.edu.ec/"#Sitio de almacenamiento
    link = ".png"#formato de la imagen
    nombre = nombre.lower().split(" ")
    apellido = apellido.lower().split(" ")
    chars = ["_"]
    nuevo_nombre = nombre[0] + random.choice(chars) + apellido[0]
    
    if duplicateFound:
        num = random.randint(0,100)
        nuevo_nombre = nuevo_nombre + str(num)
    
    return url + nuevo_nombre + link
#Arrays para guardar los emails y urls de las fotos
emails = []
fotos=[]
index = 0
#Creacion de los emails y urls de las fotos
for nombre in df['nombre']:
    apellido = df.loc[index]['apellido']#Obtener el apellido de la misma posicion que el nombre en el registro
    index += 1
    email = emailGen(nombre,apellido)
    foto = fotoGen(nombre,apellido)
    while email in emails:
        email = emailGen(nombre,apellido,duplicateFound=True)
        foto = fotoGen(nombre,apellido,duplicateFound=True)
    
    emails.append(email)#Añadir el email al array de email
    fotos.append(foto)#Añadir el url al array de urls

df['email'] = emails#Asignar los datos del array de email a la columna "email" del dataframe
df['foto'] = fotos#Asignar los datos del array de urls a la columna "foto" del dataframe

def random_dob(start, end, n):
    """
    Funcion para generar fechas de nacimiento de acuerdo a 2 fechas que funcionan como limites.

    Parametros
    ----------

        start : str
            
            Variable tipo String de la fecha maxima que espera  la función.

        end : str
            
            Variable tipo String de la fecha minima que espera  la función.

        n : int
            
            Variable tipo int que tiene el numero total de registros a crear.

    Retorna
    -------

        Retornara un array con diferentes fechas de nacimiento.

    """
    frmt = "%Y-%m-%d"
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    td = etime - stime
    times = [(random.random() * td + stime).strftime(frmt) for _ in range(n)]
    return times

#Generacion aleatoria de fechas de nacimiento de los estudiantes
df['fecha_de_nacimiento'] = random_dob("2017-09-01","2020-09-01",num_usuarios)

def edadGen(fecha):
    """
    Funcion para devolver la edad de acuerdo a su fecha de nacimiento.

    Parametros
    ----------

        fecha : str
            
            Variable tipo String de la fecha de nacimiento que espera  la función.


    Retorna
    -------

        Retornara un int con la edad.

    """
    frmt = "%Y-%m-%d"
    Actualidad = datetime.datetime.today()
    nac = datetime.datetime.strptime(fecha, frmt)
    edad = Actualidad.year - nac.year - ((Actualidad.month, Actualidad.day) < (nac.month, nac.day))
    return edad

#Generacion de las edades de los estudiantes
df['edad'] = [edadGen(i) for i in df['fecha_de_nacimiento']]

def nivelGen(edad):
    """
    Funcion para devolver el nivel del estudiante de acuerdo a su edad.

    Parametros
    ----------

        edad : int
            
            Variable tipo int de la edad del estudiante que espera la función.


    Retorna
    -------

        Retornara un string con el nivel academico.

    """
    if edad <= 3:
        return "1 nivel"
    else:
        return "2 nivel"

#Generacion de los niveles academicos de los estudiantes
df['nivel_academico'] = [nivelGen(i) for i in df['edad']]

#Generacion del archivo Estudiantes.csv donde se guardaran los datos
df.to_csv('Estudiantes.csv')
"""
Definicion de los atributos de la entidad Docente

ID(id)=El id del docente que sera unico para cada uno
Nombre(nombre)=El nombre del docente generado aleatoriamente.
Apellido(apellido)=El apellido del docente generado aleatoriamente.
Edad(edad)=La edad del docente.
Genero(genero)=El genero del docente que sera masculino o femenino.
Titulo(titulo)=El titulo del docente que puede ser entre Bachillerato,Licenciado,Tecnologo,Maestria o Doctorado.
Fecha de Nacimiento(fecha_de_nacimiento)=La fecha de nacimiento del docente.
Email(email)=Un email del docente que servira para ingresar al sistema.

"""
caracteristicas = [
    "id" ,
    "nombre" ,
    "apellido" ,
    "edad" ,
    "genero" ,
    "Titulo",
    "fecha_de_nacimiento" ,
    "email"
    ]
#Elaboración del dataframe
df = pd.DataFrame(columns=caracteristicas)

#Generacion aleatoria de los ids de los Docentes
df['id'] = [uuid.uuid4().hex for i in range(num_usuarios)]
#Generacion aleatoria del genero de los Docentes
df['genero'] = random.choices(
    generos,
    k=num_usuarios
    )
#Generacion de los nombres de los Docentes
df['nombre'] = [nombre_gen(i) for i in df['genero']]
#Generacion de los apellidos de los Docentes
df['apellido'] = [faker.last_name() for i in df['genero']]
def emailGenD(nombre,apellido,duplicateFound=False):
    """
    Funcion para generar emails aleatorios de acuerdo al nombre y apellido del docente.

    Parametros
    ----------

        nombre : str
            
            Variable tipo String del nombre del docente que espera  la función.

        apellido : str
            
            Variable tipo String del apellido del docente que espera  la función.

        duplicateFound : bool
            
            Variable tipo Bool que funcionara para identificar duplicados.

    Retorna
    -------

        Retornara el email del docente de acuerdo a sus datos.

    """
    dom = "@educacion.edu.ec"#Dominio de la institucion academica
    nombre = nombre.lower().split(" ")
    apellido = apellido.lower().split(" ")
    chars = [".","_"]
    nuevo_nombre = nombre[0] + random.choice(chars) + apellido[0]
    
    if duplicateFound:
        num = random.randint(0,100)
        nuevo_nombre = nuevo_nombre + str(num)
    
    return nuevo_nombre + "_docente" + dom#identificador de que es docente
emails = []
index = 0
for nombre in df['nombre']:
    apellido = df.loc[index]['apellido']
    index += 1
    email = emailGenD(nombre,apellido)
    while email in emails:
        email = emailGenD(nombre,apellido,duplicateFound=True)
    
    emails.append(email)
df['email'] = emails
#Generacion aleatoria de los titulos de los Docentes
titulos = ["Bachillerato","Licenciado","Tecnologo","Maestria","Doctorado"]
df['Titulo'] = random.choices(
    titulos,
    weights=(20,30,20,20,10),
    k=num_usuarios
    )
#Generacion aleatoria de las fechas de nacimiento de los docentes
df['fecha_de_nacimiento'] = random_dob("1973-01-01","1997-12-31",num_usuarios)
#Generacion de las edades de los docentes
df['edad'] = [edadGen(i) for i in df['fecha_de_nacimiento']]

#Generacion del archivo Docentes.csv donde se guardaran los datos
df.to_csv('Docentes.csv')

"""
Definicion de los atributos de la entidad Materia

ID(id)=El id de la materia que sera unico para cada una
Materia(Materia)=El nombre de la materia generado aleatoriamente.
Descripcion(Descripcion)=Descripcion de la materia generado aleatoriamente.
Estado(Status)=El estado en el que se encuentra la materia como activo o inactivo.
Periodo Academico(Periodo)=El periodo academico de la materia.

"""
caracteristicas = [
    "id" ,
    "Materia" ,
    "Descripcion" ,
    "Status" ,
    "Periodo"
    ]
#Generacion del dataframe
df = pd.DataFrame(columns=caracteristicas)
#Generacion aleatoria de los ids de las materias
df['id'] = [uuid.uuid4().hex for i in range(num_usuarios)]
#Generacion aleatoria de las materias
materias = ["Educación SocioEmocional","Exploración y Comprensión del mundo natural y social","Lenguaje y Comunicación","Artes","Pensamiento Matemáico","Educación Fisica"]
df['Materia'] = random.choices(
    materias,
    weights=(17,16,16,16,16,16),
    k=num_usuarios
    )
#Generacion aleatoria de la descripcion de la materia
df['Descripcion'] = [faker.sentence() for i in df['Materia']]
#Generacion aleatoria del periodo de la materia
periodos =["Periodo 2022-2023","Periodo 2021-2022","Periodo 2020-2021","Periodo 2019-2020","Periodo 2018-2019","Periodo 2017-2018","Periodo 2016-2017","Periodo 2015-2026","Periodo 2014-2015","Periodo 2013-2014","Periodo 2012-2013","Periodo 2011-2012","Periodo 2010-2011","Periodo 2009-2010","Periodo 2008-2009","Periodo 2007-2008","Periodo 2006-2007","Periodo 2005-2006","Periodo 2004-2005","Periodo 2003-2004","Periodo 2002-2003","Periodo 2001-2002","Periodo 2000-2001","Periodo 1999-2000"]
df['Periodo'] = random.choices(
    periodos,
    k=num_usuarios
    )
def status_gen(Periodo):
    """
    Funcion para devolver el estado en base del periodo.

    Parametros
    ----------

        Periodo : str
            
            Variable tipo String del periodo que espera  la función.


    Retorna
    -------

        Retornara el estado de acuerdo a si se esta cursando el Periodo academico actual.

    """
    if Periodo=='Periodo 2022-2023':
        return "Activo"
    else:
        return "Inactivo"

#Generacion del estado de la materia
df['Status'] = [status_gen(i) for i in df['Periodo']]
#Generacion del archivo Materias.csv donde se guardaran los datos
df.to_csv('Materias.csv')
"""
Definicion de los atributos de la entidad Aula

ID(id)=El id del aula que sera unico para cada una
Aula(Aula)=El numero del aula generado aleatoriamente en base al bloque.
Bloque(Bloque)=El bloque del aula generado aleatoriamente.
Descripcion(Descripcion)=Descripcion del aula generado aleatoriamente.
Estado(Status)=El estado en el que se encuentra el aula como activo o inactivo.
Periodo Academico(Periodo)=El periodo academico donde se esta utilizando el aula.

"""
caracteristicas = [
    "id" ,
    "Aula" ,
    "Bloque",
    "Descripcion" ,
    "Status" ,
    "Periodo"
    ]
#Generacion del dataframe
df = pd.DataFrame(columns=caracteristicas)
#Generacion aleatoria de las ids de las aulas
df['id'] = [uuid.uuid4().hex for i in range(num_usuarios)]
#Generacion aleatoria del bloque de las aulas
bloques = ["A","B","C","D","Coliseo","Patio","Salon Interactivo"]
df['Bloque'] = random.choices(
    bloques,
    k=num_usuarios
    )
def aula_gen(bloque):
    """
    Funcion para devolver el numero del aula en base del bloque.

    Parametros
    ----------

        bloque : str
            
            Variable tipo String del bloque que espera  la función.


    Retorna
    -------

        Retornara el numero del aula acuerdo al bloque en donde se encuentra.

    """
    if bloque=='A':
        num = random.randint(1,100)
        return "A-" + str(num)
    elif bloque=='B':
        num = random.randint(101,200)
        return "B-" + str(num)
    elif bloque=='C':
        num = random.randint(201,300)
        return "C-" + str(num)
    elif bloque=='D':
        num = random.randint(301,400)
        return "D-" + str(num)
    elif bloque=='Coliseo':
        return "Coliseo"
    elif bloque=='Patio':
        return "Patio"
    elif bloque=='Salon Interactivo':
        return "Salon Interactivo"
#Generacion del numero del aula
df['Aula'] = [aula_gen(i) for i in df['Bloque']]
#Generacion aleatoria de la descripcion del aula
df['Descripcion'] = [faker.sentence() for i in df['Bloque']]
#Generacion aleatoria del periodo academico del aula
periodos =["Periodo 2022-2023","Periodo 2021-2022","Periodo 2020-2021","Periodo 2019-2020","Periodo 2018-2019","Periodo 2017-2018","Periodo 2016-2017","Periodo 2015-2026","Periodo 2014-2015","Periodo 2013-2014","Periodo 2012-2013","Periodo 2011-2012","Periodo 2010-2011","Periodo 2009-2010","Periodo 2008-2009","Periodo 2007-2008","Periodo 2006-2007","Periodo 2005-2006","Periodo 2004-2005","Periodo 2003-2004","Periodo 2002-2003","Periodo 2001-2002","Periodo 2000-2001","Periodo 1999-2000"]
df['Periodo'] = random.choices(
    periodos,
    k=num_usuarios
    )
#Generacion del estado del aula de acuerdo al periodo
df['Status'] = [status_gen(i) for i in df['Periodo']]
#Generacion del archivo Aulas.csv donde se guardaran los datos
df.to_csv('Aulas.csv')