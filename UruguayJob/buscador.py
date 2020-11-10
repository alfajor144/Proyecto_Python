#-*- coding: utf-8 -*-
import os

def nombreJson(nombre):
    dir_raiz = './'
    nombre_actual = None
    valor_actual = 0
    with os.scandir(dir_raiz) as ficheros:
        ficheros = [fichero.name for fichero in ficheros if fichero.is_file() and fichero.name.endswith('.json')]
    for fichero in ficheros:
        if nombre in fichero :
            parte1 = fichero.split('_')
            parte2 = parte1[1].split('.')
            try:
                valor_fichero = int(parte2[0])
                if valor_fichero > valor_actual:
                    nombre_actual = fichero
                    valor_actual = valor_fichero
            except ValueError as error:
                print(f'No se pudo convertir a el string {parte2[0]} a int. Error: {error}')
                return None
            except :
                print(f'Error desconocido al buscar el fichero {nombre}')
                return None
        
    if nombre_actual is None:
        print(f'No se encontró ningún fichero con el nombre "{nombre}_fechaHora.json"')
    else:
        print(f'El fichero más reciente para "{nombre}" es: "{nombre_actual}"')
    return nombre_actual
    
nombreJson('concursa-ofertas_')
nombreJson('uybuscojob-ofertas_')
nombreJson('twago-ofertas_')
nombreJson('twago-perfiles_')
