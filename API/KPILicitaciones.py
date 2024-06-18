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
eCommerce_solicitudLicitacion = [connection_url_SanManuel, ecommerce_main, 'solicitudLicitacion']

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

def getDate(date:str)-> datetime.datetime:
    """date es una fecha compatible con 'dd-mm-yyyy' """
    fecha_obj = datetime.datetime.strptime(date, '%d-%m-%Y')
    y = fecha_obj.year
    m = fecha_obj.month
    d = fecha_obj.day
    return datetime.datetime(y, m, d)


def consultaLicitaciones(initial_date:str, end_date:str):
    """
    Que licitaciones he realizado en un periodo de tiempo
    """
    #convert str to datetime
    fecha_inicio = getDate(initial_date)
    fecha_fin = getDate(end_date)
    pipeline = [
                    # step 1: filter data in range of dates
                    {
                        '$match': {
                            'fecha': {
                                '$gte': fecha_inicio,
                                '$lte': fecha_fin
                            }
                        }
                    },
                    # Descomponer la lista de diccionarios en registros con cada diccioanrio
                    {
                        '$unwind': '$solicitud'
                    },
                    #agrupar los registros
                    {
                        '$group': {
                            '_id': '$solicitud.nombre',
                            'cantidadTotal': {
                                '$sum':'$solicitud.cantidad'
                            }
                        }
                    }
                 ]
    #Conection to DB
    rentabilidad_solicitudLicitacion = coneccionDB(*eCommerce_solicitudLicitacion)

    #implementacion del pipeline
    resultado = list(rentabilidad_solicitudLicitacion.aggregate(pipeline=pipeline))

    # total = resultado[0]["cantidadTotal"]
    return resultado


# a =  consultaLicitaciones(initial_date='01-05-2024', end_date='01-06-2024')
# print(a)

