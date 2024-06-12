import datetime
import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv
ruta_actual = os.getcwd() 
ruta_padre = os.path.dirname(ruta_actual)
load_dotenv('venv/.env')
import datetime
import random
import json


### Conecciona BD 
connection_url_SanManuel = os.getenv('connection_url_SanManuel')
ecommerce_main = os.getenv('ecommerce_main')
eCommerce_rentabilidad_output = [connection_url_SanManuel, ecommerce_main, 'rentabilidad_output']

####

def coneccionDB(mongo_uri:str,database_name:str,collection_name:str):
    '''Permite realizar una coneccion a una colecccion en base de datos'''
    
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        print(f'coneccion exitosa a la coleccion: {database_name}.{collection_name}')
    except Exception as e:
        print(e)
    return collection

rentabilidad_output_collection = coneccionDB(*eCommerce_rentabilidad_output)


## total de algo 
fecha_inicio = datetime.datetime(2024, 1, 1)
fecha_fin = datetime.datetime(2024, 2, 29)

# Crear el pipeline de agregación
pipeline = [
    # Paso 1: Filtrar documentos por el rango de fechas
    {
        '$match': {
            'fechaRegistro': {
                '$gte': fecha_inicio,
                '$lte': fecha_fin
            }
        }
    },
    # Paso 2: Sumar los valores de totales['unidades']
    {
        '$group': {
            '_id': None,
            'total_unidades': {
                '$sum': '$totales.unidades'
            }
        }
    }
]

# Ejecutar la agregación
resultado = list(rentabilidad_output_collection.aggregate(pipeline))

print(resultado)