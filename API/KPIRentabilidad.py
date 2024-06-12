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

def getDate(date:str)-> datetime.datetime:
    """date es una fecha compatible con 'dd-mm-yyyy' """
    fecha_obj = datetime.datetime.strptime(date, '%d-%m-%Y')
    y = fecha_obj.year
    m = fecha_obj.month
    d = fecha_obj.day
    return datetime.datetime(y, m, d)




def gastoAcumuladoChat(concepto:str, initial_date: str, end_date:str):
    """
    Regresa el total acumulado en un concepto de la categoria globales. 
        * importeMNAduana
        * flete
        * unidad
        * total
        * importeUSD
        * importeMN
        * despachoAduanalMN
        * fleteMarinoTerrestre
        * seguro
        * cuentaAduanera
        * certificaciion
        * prevalidacion
        * importeDTA
        * importeIGI
        * importeIVA
        * importe
    initial_date debe de estar en formato 'aaaa-mm-dd'
    """
    etiqueta_total = f"total_{concepto}"
    #conecction to db
    rentabilidad_output_collection = coneccionDB(*eCommerce_rentabilidad_output)
    #convert str to datetime
    fecha_inicio = getDate(initial_date)
    fecha_fin = getDate(end_date)

    pipeline = [
        # step 1: filter data in range of dates
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
                etiqueta_total: {
                    '$sum': f'$totales.{concepto}'
                }
            }
        }
    ]
    resultado = list(rentabilidad_output_collection.aggregate(pipeline))
    total = resultado[0][f"total_{concepto}"]
    total_format = format(total, ",.2f")
    msg = "El gasto acumulado por el concepto de {} en el periodo que comprende del {} al {} es de {} ".format(concepto,initial_date,end_date,total_format)
    return msg

######################
print("***"*30)

# respuesta = gastoAcumuladoChat(concepto='importeUSD', initial_date='12-01-2024', end_date='16-06-2024')
# print(respuesta)