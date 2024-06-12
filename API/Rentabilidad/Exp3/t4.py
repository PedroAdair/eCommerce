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

from func2 import *
connection_url_SanManuel = os.getenv('connection_url_SanManuel')
ecommerce_main = os.getenv('ecommerce_main')
eCommerce_rentabilidad_output = [connection_url_SanManuel, ecommerce_main, 'rentabilidad_output']
eCommerce_rentabilidad_input = [connection_url_SanManuel, ecommerce_main, 'rentabilidad_input']

######################################################################################################################
#from faker import Faker    esa luego eliminarla. Es para crear datos al azar
from faker import Faker
fake = Faker()

#datos originales
with open('API/Rentabilidad/Exp3/opciones_productos.json', 'r') as archivo_json:
    opciones_productos = json.load(archivo_json)

start = datetime.datetime(2024,1,1)
end =  datetime.datetime(2024,6,10)


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




def fecha_aleatoria(inicio, fin):
    delta = fin - inicio
    dias_aleatorios = random.randint(0, delta.days)
    return inicio + datetime.timedelta(days=dias_aleatorios)
# print(new_reg['productos'][0].keys())



def registroProducto(product:dict):
    unidades         = random.randint(100, 40000)
    importeMNAduana  = unidades*random.uniform(10,12)
    flete            = unidades*random.uniform(1.5,2.7)

    estructura= {
            "informacionGeneral":{
                "claveProducto": product["Clave del Producto y/o Servicio"],
                "descripcionProducto":product["Descripción Producto según Pedimento"],
                "piezas":product["Piezas"]
            },
            "datosPedimiento":{
                "importeMNAduana": importeMNAduana,
                "flete": flete,
                "unidades": unidades
            },
            "A1":{
                "costoUnitarioUSD": product['Costo Unit.  USD (Mcía.)']
            },
            "A2":{
            },
            "A3":{
            },
            "A4":{
            },
            "A5":{
            },
            "A6":{
            },
            "A7":{
                "valor_prevalidacion": 1,
                "porcentajeDTA":8
            },
            "A8":{
                "porcentajeIGI": random.choice([10,20,25])
            },
            "A9": {
            },
            "costoTotal":{
    
            },
            "B2":{
                "precioVentaPropuesto": product['Costo Unit.  USD (Mcía.)']*17*2
            },
            "propuestaPropia":{
                "precioVentaPropuesto": product['Costo Unit.  USD (Mcía.)']*17*2.7
            },
            "propuestaSuperior":{
                "precioVentaPropuesto":product['Costo Unit.  USD (Mcía.)']*17*3
            }
        }
    return estructura

def creafFalsoRegistro():
    rentabilidad_output_collection = coneccionDB(*eCommerce_rentabilidad_output)
    result = {}
    result["tipoCambio"]= {"historial": [
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
    res1 = result.copy()

    number_items =  random.randint(1,len(opciones_productos))
    print(f"Se realizara una simulacion de {number_items} producto/s")
    producrtos_aleatorios = random.sample(opciones_productos, number_items)
    products_list = []
    for product in producrtos_aleatorios:
        products_list.append(registroProducto(product=product))

    result["productos"] = products_list
    result['totales']= {}
    result = pipelineCompleto(rentabilidad=result)
    # result.update(res1)
    result['fechaRegistro'] = fecha_aleatoria(inicio=start, fin=end)


    #
    total_registros = rentabilidad_output_collection.count_documents({})
    print(f"Hay un total de {total_registros} registros")
    result['id']= total_registros +1
    rentabilidad_output_collection.insert_one(result)
    return result

print("**"*50)
for i in range(10):
    creafFalsoRegistro()
