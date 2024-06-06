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

def actualizarDatosPedimiento(products:dict):
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
    totalUnidades = products['totales']['unidades']

    #optener el precio en moneda mexicana considerando el tipo de cambio por la compra
    importesUSD = lambda x: {**x, 'A1': {**x['A1'], 'importeMN': round(x['A1']['importeUSD']*tipoCambio,2)}}
    products['productos'] = list(map(importesUSD, products["productos"]))
    #costoUnitarioMN
    costoUnitarioMN = lambda x: {**x, 'A1': {**x['A1'], 'costoUnitarioMN': round(x['A1']['importeMN']/x['datosPedimiento']['unidades'],2)}}
    products['productos'] = list(map(costoUnitarioMN, products["productos"]))

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

#############################################################################################################################################################################
#A3
#############################################################################################################################################################################
def obtenerA3(payments:dict, products:dict):
    """flete"""
    flete         = payments['tipoCambio']['globales']['flete']
    totalUnidades = products['totales']['unidades']

    fletesMarinoTerrestre = lambda x: {**x, 'A3': {**x['A3'], 'fleteMarinoTerrestre': round(flete/totalUnidades*x['datosPedimiento']['unidades'],2)}}
    products['productos'] = list(map(fletesMarinoTerrestre, products["productos"]))
    
    fleteUnitValue = round(flete/totalUnidades,2)
    fleteUnit = lambda x: {**x, 'A3': {**x['A3'], 'fleteUnit': fleteUnitValue}}
    products['productos'] = list(map(fleteUnit, products["productos"]))

    totales_fleteMarinoTerrestre = round(sum(map(lambda x: x["A3"]["fleteMarinoTerrestre"], products["productos"])),2)
    products['totales']["fleteMarinoTerrestre"] = totales_fleteMarinoTerrestre

    return products

#############################################################################################################################################################################
#A4
#############################################################################################################################################################################
def obtenerA4(payments:dict, products:dict):
    """seguro"""
    seguro = payments['tipoCambio']['globales']['seguro']
    totalUnidades = products['totales']['unidades']
    seguroValue = round(seguro/totalUnidades,3)

    fletesMarinoTerrestre = lambda x: {**x, 'A4': {**x['A4'], 'seguro': round(seguroValue*x['datosPedimiento']['unidades'],2)}}
    
    products['productos'] = list(map(fletesMarinoTerrestre, products["productos"]))
    
    fleteUnit = lambda x: {**x, 'A4': {**x['A4'], 'seguroUnit': seguroValue}}
    products['productos'] = list(map(fleteUnit, products["productos"]))

    totales_seguro = round(sum(map(lambda x: x["A4"]["seguro"], products["productos"])),2)
    products['totales']["seguro"] = totales_seguro

    return products
#############################################################################################################################################################################
#A5
#############################################################################################################################################################################

def obtenerA5(payments:dict, products:dict):
    """ cuenta Aduanera"""
    cuentaAduanera = payments['tipoCambio']['globales']['cuentaAduanera']
    totalUnidades = products['totales']['unidades']
    cuentaAduaneraValue = round(cuentaAduanera/totalUnidades,3)

    cuentasAduanera = lambda x: {**x, 'A5': {**x['A5'], 'otrosCuentaAduanera': round(cuentaAduaneraValue*x['datosPedimiento']['unidades'],2)}}
    
    products['productos'] = list(map(cuentasAduanera, products["productos"]))
    
    fleteUnit = lambda x: {**x, 'A5': {**x['A5'], 'otrosUnit': cuentaAduaneraValue}}
    products['productos'] = list(map(fleteUnit, products["productos"]))

    totales_cuentaAduanera = round(sum(map(lambda x: x["A5"]["otrosCuentaAduanera"], products["productos"])),2)
    products['totales']["cuentaAduanera"] = totales_cuentaAduanera

    return products

#############################################################################################################################################################################
#A6
#############################################################################################################################################################################
def obtenerA6(payments:dict, products:dict):
    """Certificaciones"""
    certificaciones = payments['tipoCambio']['globales']['certificaciones']
    totalUnidades = products['totales']['unidades']
    certificacionesValue = round(certificaciones/totalUnidades,3)

    certificaciones = lambda x: {**x, 'A6': {**x['A6'], 'certificaciones': round(certificacionesValue*x['datosPedimiento']['unidades'],2)}}
    
    products['productos'] = list(map(certificaciones, products["productos"]))
    
    fleteUnit = lambda x: {**x, 'A6': {**x['A6'], 'certificacionesUnit': certificacionesValue}}
    products['productos'] = list(map(fleteUnit, products["productos"]))

    totales_certificaciones = round(sum(map(lambda x: x["A6"]["certificaciones"], products["productos"])),2)
    products['totales']["certificaciones"] = totales_certificaciones

    return products

#############################################################################################################################################################################
#A6
#############################################################################################################################################################################
def obtenerA7(payments:dict, products:dict):
    """prevalidacion y DTA"""
    prevalidacion = payments['tipoCambio']['globales']['prevalidacion']
    #prevalidacion
    prevalidaciones = lambda x: {**x, 'A7': {**x['A7'], 'prevalidacion': round(prevalidacion*x['A7']['valor_prevalidacion'],2)}}
    products['productos'] = list(map(prevalidaciones, products["productos"]))
    #totslPrevalidaciones
    totales_prevalidaciones = round(sum(map(lambda x: x["A7"]["prevalidacion"], products["productos"])),2)
    products['totales']["prevalidacion"] = totales_prevalidaciones
    #prevalidacionUnit
    prevalidacionesUnit = lambda x: {**x, 'A7': {**x['A7'], 'prevalidacionUnit': round(x['A7']['prevalidacion']/x['datosPedimiento']['unidades'],2)}}
    products['productos'] = list(map(prevalidacionesUnit, products["productos"]))
    #DTA
    prevalidacionesUnit = lambda x: {**x, 'A7': {**x['A7'], 'DTA': round((x['A7']['porcentajeDTA']/100)*x['datosPedimiento']['costoUnitario'],3)}}
    products['productos'] = list(map(prevalidacionesUnit, products["productos"]))
    
    #importe DTA
    importeDTA = lambda x: {**x, 'A7': {**x['A7'], 'importeDTA': round((x['A7']['DTA'])*x['datosPedimiento']['unidades'],3)}}
    products['productos'] = list(map(importeDTA, products["productos"]))
    totales_DTA = round(sum(map(lambda x: x["A7"]["importeDTA"], products["productos"])),2)
    products['totales']["importeDTA"] = totales_DTA

    
    return products





############################################################################################################################################################################
# Pagos
############################################################################################################################################################################
def registrarPrimerPago(payments:dict):
    tipoCambio = round(np.mean(np.array(list(map(lambda x: x["tipoCambio"], payments["tipoCambio"]["historial"])))),3)
    payments['tipoCambio']['globales']['tipoCambio'] = tipoCambio
    return payments

############################################################################################################################################################################

def obtenerSubtotalIndividual(product:dict):
    """Obtener dubtosles po producto A1-A6"""
    costoUnitarioMN       = product['A1']['costoUnitarioMN']
    despachoAduanalMNUnit = product['A2']['despachoAduanalMNUnit']
    fleteUnit             = product['A3']['fleteUnit']
    seguroUnit            = product['A4']['seguroUnit']
    otrosUnit             = product['A5']['otrosUnit']
    certificacionesUnit   = product['A6']['certificacionesUnit']

    subtotal = np.sum([costoUnitarioMN, despachoAduanalMNUnit, fleteUnit, seguroUnit, otrosUnit, certificacionesUnit])
    
    return subtotal

def obtenerSubtotal(payments:dict, products:dict):
    """subtotales"""
    
    # subtotales = lambda x: {**x, 'costoTotal': {**x['costoTotal']['subtotal'], 'subtotal': }}

    subtotales = lambda x: {**x, 'costoTotal': {**x['costoTotal'], 'subtotal': round(obtenerSubtotalIndividual(product=x),2)}}
    
    products['productos'] = list(map(subtotales, products["productos"]))
    
    # fleteUnit = lambda x: {**x, 'A6': {**x['A6'], 'certificacionesUnit': certificacionesValue}}
    # products['productos'] = list(map(fleteUnit, products["productos"]))

    # totales_certificaciones = round(sum(map(lambda x: x["A6"]["certificaciones"], products["productos"])),2)
    # products['totales']["certificaciones"] = totales_certificaciones

    return products
#############################################################################################################################################################################
# Proceso
#############################################################################################################################################################################
print("*"*150)
#paso 1. registrar los productos con su primeras caracteristicas
products = actualizarDatosPedimiento(products=products)
#paso 2. registrar el primer pago
payments = registrarPrimerPago(payments=payments)
#Paso 3
products = obtenerA1(payments=payments, products=products)
#paso 4 Obtener A2
products = obtenerA2(payments=payments ,products=products)
#Paso 5 Obtener A3 (fletes)
products = obtenerA3(payments=payments ,products=products)
#Paso 6 Obtener A4 (seguro)
products = obtenerA4(payments=payments ,products=products)
#Paso 7 Obtener A5 (seguro)
products = obtenerA5(payments=payments ,products=products)
#Paso 8 Obtener A6 (seguro)
products = obtenerA6(payments=payments ,products=products)
#Paso 9. Obtener costos subtotlles de producto
products = obtenerSubtotal(payments=payments ,products=products)
#paso 10. Obtener las prevalidaciones.
products = obtenerA7(payments=payments ,products=products)


print("Ejemplo de un producto")
print(products['productos'][0]) 
print("**"*100)
print("totales")
print(products['totales'])     
# aa = list(map(lambda x: x['A1'].update({'importeMN': x['A1']['importeUSD']*tipoCambio}), products["productos"]))
# print(aa)

print("**"*100)
print("Pagos")
print(payments['tipoCambio']['globales'])