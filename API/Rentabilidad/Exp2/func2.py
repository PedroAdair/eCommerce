from pymongo import MongoClient
import pymongo
from bson import ObjectId
import pandas as pd
from dotenv import load_dotenv
load_dotenv('venv/.env')
import os
import json
import numpy

with open('DB_examples/primerinputProductos.json', 'r') as f:

    products =  json.loads(f.read())

print(products)



def getDatosPedimiento(product:dict):
    total = product['datosPedimiento']["importeMNAduana"] + product['datosPedimiento']["flete"]
    product['datosPedimiento']["total"] = total
    product['datosPedimiento']["costoUnitario"] = round(total/product['datosPedimiento']['unidades'], 2)
    return product

def getCompleteDatosPedimiento(products:dict):
    datosPedimiento = map(lambda x: getDatosPedimiento(x), products["productos"])
    products["productos"] = list(datosPedimiento)
    totales_importeMNAduana = round(sum(map(lambda x: x['datosPedimiento']['importeMNAduana'], products["productos"])),2)
    totales_flete = round(sum(map(lambda x: x['datosPedimiento']['flete'], products["productos"])),2)
    totales_unidades = sum(map(lambda x: x['datosPedimiento']['unidades'], products["productos"]))
    totales_total = sum(map(lambda x: x['datosPedimiento']['total'], products["productos"]))


    totales = {"importeMNAduana": totales_importeMNAduana,
            "flete": totales_flete,
            "unidades": totales_unidades,
            "total": totales_total
            }


    products["totales"] = totales

    return products

######################################################################################


def getTotalImporteUSD(products:dict):
    for x in products["productos"]:
        x["A1"]["importeUSD"] =  x["A1"]["costoUnitarioUSD"]*x['datosPedimiento']['unidades']

    totales_importeUSD = sum(map(lambda x: x["A1"]["importeUSD"], products["productos"]))

    products["importeUSD"] = totales_importeUSD
    return products


print("*"*150)
products = getCompleteDatosPedimiento(products=products)
products = getTotalImporteUSD(products=products)


print(products)
# print(list(importeUSD))
# products = getTotalImporteUSA(products=products)

# # print(products["productos"])
# for product in products['productos']:
#     print(product["A1"])

