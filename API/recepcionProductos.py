from pymongo import MongoClient
import pymongo
from bson import ObjectId
import pandas as pd
from dotenv import load_dotenv
load_dotenv('venv/.env')
import os
import logging
import datetime
logging.basicConfig(filename='log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def coneccionDB(mongo_uri:str,database_name:str,collection_name:str):
    '''Permite realizar una coneccion a una colecccion en base de datos'''
    
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        print(f'coneccion exitosa a la coleccion: {database_name}.{collection_name}')
        return collection
    except Exception as e:
        print(e)


def findElements(_id_recepcion_producto:str, _id_solicitud_compra:str):
    """
    Dados los string de las id de los productos, se comprieba
    """
    try:
        solicitudes_compra = coneccionDB(os.getenv('connection_url_SanManuel'), os.getenv('ecommerce_ds'), os.getenv('solicitudes_compra'))
        recepcion_productos = coneccionDB(os.getenv('connection_url_SanManuel'), os.getenv('ecommerce_ds'), os.getenv('recepcion_productos'))

        #realizar busqueda en BD
        solicitud_compra = solicitudes_compra.find_one({"_id": ObjectId(_id_solicitud_compra)})
        producto = recepcion_productos.find_one({"_id": ObjectId(_id_recepcion_producto)})
        if solicitud_compra == None or producto == None:
            return "Error", "Dato no encontrado en la coleccion", -1
        else: 
            return solicitud_compra, producto, 0
    except Exception as e:
        logging.error(str(e))
        print(e)
        return "Error", " Busqueda fallida", -1


def Compare(solicitud_compra, producto, val):
    if val == 0:
        """Verificar que la orden de compra coincide"""

        id_order_soli = solicitud_compra['id_order']
        id_order_prod = producto['id_order']

        if id_order_prod == id_order_soli:
            print("todo correcto, coincide el id de la solicutud y de la  informacion recibida")
            ########################################################################################
            json_order  = solicitud_compra['products']
            list_records = producto['products']
            df_o = pd.DataFrame(list_records)
            resultado = df_o.drop_duplicates().groupby('sku')['serial_num'].size().reset_index(name='registrados')
            resultado.set_index('sku', inplace=True)
            df = pd.DataFrame(json_order)
            df.set_index('sku', inplace=True)
            df['registrados'] = resultado['registrados']
            ########################################################################################
    
            #Results
            mask_diferentes = df['cantidad'] != df['registrados']
            non_equal = df[mask_diferentes]
            equal = df[~mask_diferentes]
            return equal, non_equal, 0
        else:
            return "Error", "Los ids corresponden a productos con ordenes diferentes", 1

    else:
        print("{}, {}".format(solicitud_compra, producto))
        return "Error", producto , 1
    


def generateMsg(equal:pd.DataFrame,non_equal:pd.DataFrame, id_order: str)->dict:
    if non_equal.empty:
        
        msg_ext = "Han sido registrados de manera efectiva {} productos de {} tipos diferentes".format(sum(equal['cantidad']), equal.shape[0])
        msg_complete = msg_ext
        date_now =datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        alert = {
            "id_order": id_order,
            "msg": msg_ext,
            "msg_complete": msg_complete,
            "date": date_now,
            "level": "VoBo",
            "data": equal.to_json()
        }
    else:
        faltantes = sum(non_equal['cantidad'] - non_equal['registrados'])
        diferentes = non_equal.shape[0]

        msg_ext = "Existe una inconsistecia de {} productos faltantes de {} tipos diferentes".format(faltantes, diferentes)

        msg1 = ""
        for sku, row in non_equal.iterrows():
            msg = "Para el producto con sku {} ({}) se registraron {}, mientras que el total deberia de ser {}. ".format(sku, row['nombre'],row['registrados'], row['cantidad'] )
            msg1 += msg  + " "

        msg_complete = msg_ext + ", a continuacion se describen: " + msg1
        date_now =datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        alert = {
            "msg": msg_ext,
            "msg_complete": msg_complete,
            "date": date_now,
            "level": "warning",
            "data": non_equal.to_json()
        }

    return alert

def recepcionProductos(_id_recepcion_producto:str, _id_solicitud_compra:str, insertDB:bool=True):
    solicitud_compra, producto, val = findElements(_id_recepcion_producto=_id_recepcion_producto, _id_solicitud_compra=_id_solicitud_compra)
    equal, non_equal, val = Compare(solicitud_compra, producto, val)
    if val == 0:
        # print("DataFrame de registros completos")
        # print(equal)
        # print("*"*50)
        # print("DataFrame de registros Incompletos!!!!")
        # print(non_equal)
        id_order = solicitud_compra['id_order']
        alert = generateMsg(equal=equal, non_equal=non_equal,id_order=id_order)
        # return alert
        # print(alert)
        
        if True:
            alert_c = alert.copy()
            alerts = coneccionDB(os.getenv('connection_url_SanManuel'), os.getenv('ecommerce_ds'), os.getenv('alerts'))
            alerts.insert_one(alert_c)
        return alert
    else:
        print("{}, {}".format(equal, non_equal))
        return {"msg": "{}, {}".format(equal, non_equal)}
    

# recepcionProductos(_id_recepcion_producto = '66578d3e7ab7565423a85e11', _id_solicitud_compra = '665787757ab7565423a85dee')