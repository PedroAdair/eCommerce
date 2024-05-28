
import datetime
import pymongo
import schedule
import logging
import time 

from pymongo import MongoClient


logging.basicConfig(filename='database_reader.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')



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




# while True:
#     hora = 
#     print()

def count_incidents():
    try:
        collection = coneccionDB("mongodb+srv://Jocd:Constanza@constanza.lso5rqa.mongodb.net/?retryWrites=true&w=majority&appName=Constanza&tls=true", "Ecommerce","producto")
        logging.info("Existe {} registros".format(collection.count_documents({})))
    except Exception as e:
        logging.error(f'Error al leer la base de datos: {str(e)}')



schedule.every(2).seconds.do(count_incidents)

while True:
    schedule.run_pending()
    time.sleep(1) 