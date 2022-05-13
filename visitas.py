import sqlite3
import datetime
from asyncio.windows_events import NULL

"""
datetime.datetime.now().replace(microsecond=0).isoformat()

devuelve fecha hora actual en formato ISO8601 simple

yyyymmddThh:mm:ss

"""

class Persona:
    def __init__(self, dni, apellido, nombre='', movil=''):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.movil= movil


def ingresa_visita(persona):
    """Guarda los datos de una persona al ingresar"""
    conn = sqlite3.connect('recepcion.db')

    q = f"""SELECT dni FROM personas WHERE dni = '{persona.dni}'"""

    resu = conn.execute(q)

    if resu.fetchone():
        print("ya existe")
    else:
        q = f"""INSERT INTO personas (dni, nombre, apellido, movil)
                VALUES ('{persona.dni}',
                        '{persona.nombre}',
                        '{persona.apellido}',
                        '{persona.movil}');"""
        conn.execute(q)
        y = datetime.datetime.now().replace(microsecond=0).isoformat()
        
        k = f"""INSERT INTO ingresos_egresos (dni,fechahora_in,fechahora_out,destino)
                VALUES ('{persona.dni}',
                        '{y}',
                        '{NULL}',
                        '{NULL}');"""
        conn.execute(k)
        conn.commit()
     
    conn.close()
    

def egresa_visita (dni):
    """Coloca fecha y hora de egreso al visitante con dni dado"""
    conn = sqlite3.connect('recepcion.db')

    y = datetime.datetime.now().replace(microsecond=0).isoformat()

    destino = input("Destino: ")

    k = f"""INSERT INTO ingresos_egresos (dni,fechahora_in,fechahora_out,destino)
                VALUES ('{dni}',
                        '{NULL}',
                        '{y}',
                        '{destino}');"""
    
    conn.execute(k)
    conn.commit()
    conn.close()


def lista_visitantes_en_institucion ():
    """Devuelve una lista de objetos Persona presentes en la institución"""
    
    conn = sqlite3.connect('recepcion.db')

    q = f"""SELECT p.dni,nombre,apellido 
            FROM personas p
            INNER JOIN ingresos_egresos i ON p.dni = i.dni 
            WHERE fechahora_out like 0 ;"""

    print(q)
    resu = conn.execute(q)
    
    for fila in resu:
        print(fila)
    conn.close()


def busca_vistantes(fecha_desde, fecha_hasta, destino, dni):
    """ busca visitantes segun criterios """
    conn = sqlite3.connect('recepcion.db')

    q = f"""SELECT p.dni,p.nombre,p.apellido 
            FROM personas p
            INNER JOIN ingresos_egresos i ON p.dni = i.dni 
            WHERE i.dni like '{dni}' and destino like '{destino}' and fechahora_in like '{fecha_desde}' and fechahora_out like '{fecha_hasta}' ;"""
    print(q)
    
    resu = conn.execute(q)
    
    for fila in resu:
        print(fila)
    
    conn.commit()
    conn.close()



def iniciar():
    conn = sqlite3.connect('recepcion.db')

    qry = '''CREATE TABLE IF NOT EXISTS
                            personas
                    (dni TEXT NOT NULL PRIMARY KEY,
                     nombre   TEXT,
                     apellido TEXT  NOT NULL,
                     movil    TEXT  NOT NULL

           );'''

    conn.execute(qry)

    qry = '''CREATE TABLE IF NOT EXISTS
                            ingresos_egresos
                    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                     dni TEXT NOT NULL,
                     fechahora_in TEXT  NOT NULL,
                     fechahora_out TEXT,
                     destino TEXT

           );'''

    conn.execute(qry)


if __name__ == '__main__':
    iniciar()

    """
    p = Persona('28123456', 'Álavarez', 'Ana', '02352-456789')

    ingresa_visita(p)
    """
   
    """
    doc = input("Igrese dni> ")
    apellido = input("Igrese apellido> ")
    nombre = input("nombre> ")
    movil = input("móvil > ")

    p = Persona(doc, apellido, nombre, movil)
    
    ingresa_visita(p)
    """


    """
    dni = input("DNI: ")
    egresa_visita(dni)
    """


    #lista_visitantes_en_institucion()
    
    #busca_vistantes("2022-05-12T21:10:29","0","0","1")
    