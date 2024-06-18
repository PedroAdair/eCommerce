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
eCommerce_inventario = [connection_url_SanManuel, ecommerce_main, 'inventario']


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

def consultaInventario():

    rentabilidad_solicitudLicitacion = coneccionDB(*eCommerce_inventario)

    pipeline  = [
        {
            '$group': {
                '_id': '$nombreOriginal',
                'Total': {'$first': '$Total'}  
            }
        }
    ]
    resultado = list(rentabilidad_solicitudLicitacion.aggregate(pipeline=pipeline))
    return resultado

def getProduct(product_name:str):
    """ 
    obtener la informacion de un producto
    """
    eCommerce_inventario = [connection_url_SanManuel, ecommerce_main, 'inventario']
    product = coneccionDB(*eCommerce_inventario).find_one({'nombreOriginal': product_name})
    del product['_id']
    # eCommerce_inventario = [connection_url_SanManuel, ecommerce_main, 'producto']
    # product1 = coneccionDB(*eCommerce_inventario).find_one({'nombre': product_name})

    # print(product1)
    # product['foto'] = '/img/no-encontrado.png' 
    return product