from pymongo import MongoClient
import pymongo
from bson import ObjectId
import pandas as pd
from dotenv import load_dotenv
load_dotenv('venv/.env')
import os
import json
import numpy as np




with open('DB_examples/primerinputProductos.json', 'r') as f:

    products =  json.loads(f.read())

with open('DB_examples/primerinputPagos.json', 'r') as f:

    payments =  json.loads(f.read())

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

############################################################################################################################################################################
############################################################################################################################################################################


def getTotalImporteUSD(products:dict):
    for x in products["productos"]:
        x["A1"]["importeUSD"] =  x["A1"]["costoUnitarioUSD"]*x['datosPedimiento']['unidades']

    totales_importeUSD = sum(map(lambda x: x["A1"]["importeUSD"], products["productos"]))

    products['totales']["importeUSD"] = totales_importeUSD
    return products

#############################################################################################################################################################################
#A1
#############################################################################################################################################################################
def obtenerA1(payments:dict, products:dict):
    #obtener el tipo de cambio
    tipoCambio = payments['tipoCambio']['globales']['tipoCambio']
    #optener el precio en moneda mexicana considerando el tipo de cambio por la compra
    importesUSD = lambda x: {**x, 'A1': {**x['A1'], 'importeMN': round(x['A1']['importeUSD']*tipoCambio,2)}}
    products['productos'] = list(map(importesUSD, products["productos"]))

    totales_importeMN = sum(map(lambda x: x["A1"]["importeMN"], products["productos"]))
    products['totales'].update({'importeMN':totales_importeMN}) 
    return products 

#############################################################################################################################################################################
#A2
#############################################################################################################################################################################
def obtenerA2(payments:dict, products:dict):
    promedioMN = payments['tipoCambio']['globales']['MN']
    totalUnidades = products['totales']['unidades']
    #despachoAduanalMN
    despachosAduanalMN = lambda x: {**x, 'A2': {**x['A2'], 'despachoAduanalMN': round(promedioMN/totalUnidades*x['datosPedimiento']['unidades'],2)}}
    products['productos'] = list(map(despachosAduanalMN, products["productos"]))
    #despachoAduanalMNUnit
    despachosAduanalMNUnit = lambda x: {**x, 'A2': {**x['A2'], 'despachoAduanalMNUnit': round(promedioMN/totalUnidades,2)}}
    products['productos'] = list(map(despachosAduanalMNUnit, products["productos"]))
    #Obtener totales de despachoAduanal
    totales_despachoAduanalMN = round(sum(map(lambda x: x["A2"]["despachoAduanalMN"], products["productos"])),2)
    products['totales']["despachoAduanalMN"] = totales_despachoAduanalMN
    return products

############################################################################################################################################################################
# Pagos
############################################################################################################################################################################
def registrarPrimerPago(payments:dict):
    tipoCambio = round(np.mean(np.array(list(map(lambda x: x["tipoCambio"], payments["tipoCambio"]["historial"])))),3)
    payments['tipoCambio']['globales']['tipoCambio'] = tipoCambio
    return payments


#############################################################################################################################################################################
# Proceso
#############################################################################################################################################################################
print("*"*150)
#paso 1. registrar los productos con su primeras caracteristicas
#es posible unir esras funciones en una sola
products = getCompleteDatosPedimiento(products=products)
products = getTotalImporteUSD(products=products)
#paso 2. registrar el primer pago
payments = registrarPrimerPago(payments=payments)
#Paso 3
products = obtenerA1(payments=payments, products=products)
#paso 4 Obtener A2
products = obtenerA2(payments=payments ,products=products)


 
print(products['productos'][0]) 
print("**"*100)
print(products['totales'])     
# aa = list(map(lambda x: x['A1'].update({'importeMN': x['A1']['importeUSD']*tipoCambio}), products["productos"]))
# print(aa)

