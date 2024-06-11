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

# from rentabilidad import * 


connection_url_SanManuel = os.getenv('connection_url_SanManuel')
ecommerce_main = os.getenv('ecommerce_main')
eCommerce_rentabilidad_output = [connection_url_SanManuel, ecommerce_main, 'rentabilidad_output']
eCommerce_rentabilidad_input = [connection_url_SanManuel, ecommerce_main, 'rentabilidad_input']

######################################################################################################################
#from faker import Faker    esa luego eliminarla. Es para crear datos al azar
from faker import Faker
fake = Faker()

#####################################################################################################################
with open('API/Rentabilidad/Exp3/opciones_productos.json', 'r') as archivo_json:
    opciones_productos = json.load(archivo_json)

print("opciones productos")
print(len(opciones_productos))
print( random.choice(opciones_productos))


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

rentabilidad_input_collection = coneccionDB(*eCommerce_rentabilidad_input)


# def crearFalsosRegistros():
#     start = datetime.datetime(2024,1,1)
#     end = datetime.datetime(2024,6,10)
#     delta = end - start
#     int_delta = delta.days
#     random_date = random.randrange(int_delta)

#     return start + datetime.timedelta(days=random_date)

# for i in range(5):
#     print(crearFalsosRegistros())

def creafFalsoRegistro():
    registro = {}
    registro["tipoCambio"]= {"historial": [
                                            {"nombre": "Primer Pago",
                                                "concepto": "Mercancia",
                                                "tipoCambio": random.uniform(15, 19),
                                                "dolares":   random.randint(1000, 15000),
                                                "monedaNacional":random.randint(10000, 150000) }
                                        ],
                             "globales": {
                                 "porcentajeIVA":16,
                                 "MN": random.randint(10000, 150000),    
                                 "flete":random.randint(10000, 150000),
                                 "seguro": random.randint(10000, 150000),
                                 "cuentaAduanera":random.randint(10000, 150000),   
                                 "certificaciones":random.randint(1000, 15000),
                                 "prevalidacion":random.randint(10000, 150000)
                             }
                             }


    number_items =  random.randint(1,len(opciones_productos))

    return registro

print("**"*50)
registro = rentabilidad_input_collection.find_one()
new_reg =  creafFalsoRegistro(registro=registro)
# print(new_reg['productos']['informacionGeneral'])

