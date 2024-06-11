from pymongo import MongoClient
import pymongo
from bson import ObjectId
import pandas as pd
from dotenv import load_dotenv
load_dotenv('venv/.env')
import os
import json
import numpy as np






def extraerInformacion(rentabilidad:dict):
    """ payments, productos """
    payments =  {k: rentabilidad[k] for k in ('tipoCambio', 'globales') if k in rentabilidad}
    productos =  {'productos': rentabilidad['productos'],
                  'totales': rentabilidad['totales']}
    
    return payments, productos


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
#A7
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
#A8
#############################################################################################################################################################################

def obtenerA8(payments:dict, products:dict):
    """ Importe IGI"""
    IGI = lambda x: {**x, 'A8': {**x['A8'], 'IGI': round((x['A8']['porcentajeIGI'])*x['datosPedimiento']['costoUnitario']/100,3)}} 
    products['productos'] = list(map(IGI, products["productos"]))

    importeIGI = lambda x: {**x, 'A8': {**x['A8'], 'importeIGI': round((x['A8']['IGI'])*x['datosPedimiento']['unidades'],3)}} 
    products['productos'] = list(map(importeIGI, products["productos"]))

    totales_IGI = round(sum(map(lambda x: x["A8"]["importeIGI"], products["productos"])),2)
    products['totales']["importeIGI"] = totales_IGI

    return products

############################################################################################################################################################################
#A9
############################################################################################################################################################################
def calcularIVA(producto:dict, porcentajeIVA:float):
    porcentajeIVA /=100
    DTA = producto['A7']['DTA']
    IGI = producto['A8']['IGI']
    costoUnitario = producto['datosPedimiento']['costoUnitario']
    iva = (costoUnitario+DTA+IGI)*porcentajeIVA
    return iva

def obtenerA9(payments:dict, products:dict):
    """ Importe IVA"""
    porcentajeIVA = payments['tipoCambio']['globales']['porcentajeIVA']

    IVA = lambda x: {**x, 'A9': {**x['A9'], 'IVA': round(calcularIVA(producto=x, porcentajeIVA=porcentajeIVA),3)}} 
    products['productos'] = list(map(IVA, products["productos"]))

    importeIVA = lambda x: {**x, 'A9': {**x['A9'], 'importeIVA': round((x['A9']['IVA'])*x['datosPedimiento']['unidades'],3)}} 
    products['productos'] = list(map(importeIVA, products["productos"]))
    
    totales_IVA = round(sum(map(lambda x: x["A9"]["importeIVA"], products["productos"])),2)
    products['totales']["importeIVA"] = totales_IVA

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


    subtotales = lambda x: {**x, 'costoTotal': {**x['costoTotal'], 'subtotal': round(obtenerSubtotalIndividual(product=x),2)}}
    
    products['productos'] = list(map(subtotales, products["productos"]))
    

    return products
############################################################################################################################################################################
def obtenerCostoTotalIndividual(product:dict):
    prevalidacionUnit  = product['A7']['prevalidacionUnit']
    DTA                = product['A7']['DTA']
    IGI                = product['A8']['IGI']
    IVA                = product['A9']['IVA']
    subtotal           = product['costoTotal']['subtotal']

    total = np.sum([subtotal, IVA, IGI, DTA, prevalidacionUnit])
    
    return total

def obtenerImporteIndividua(product:dict):
    importeMN              = product['A1']['importeMN']
    despachoAduanalMN      = product['A2']['despachoAduanalMN']
    fleteMarinoTerrestre   = product['A3']['fleteMarinoTerrestre']
    seguro                 = product['A4']['seguro']
    otrosCuentaAduanera    = product['A5']['otrosCuentaAduanera']
    prevalidacion          = product['A7']['prevalidacion']
    importeDTA             = product['A7']['importeDTA']
    importeIGI             = product['A8']['importeIGI']
    importeIVA             = product['A9']['importeIVA']

    importe = np.sum([importeMN, despachoAduanalMN, fleteMarinoTerrestre, seguro, otrosCuentaAduanera, prevalidacion, importeDTA, importeIGI, importeIVA])
    
    return importe



def obtenerCostoTotal(payments:dict, products:dict):
    """subtotales"""


    totales = lambda x: {**x, 'costoTotal': {**x['costoTotal'], 'CostoFinal': round(obtenerCostoTotalIndividual(product=x),2)}}
    products['productos'] = list(map(totales, products["productos"]))
    # sCostoMecia 
    sCostoMecia = lambda x: {**x, 'costoTotal': {**x['costoTotal'], 'sCostoMecia': round(x['A1']['costoUnitarioMN']/x['costoTotal']['CostoFinal']*100,2)}}
    products['productos'] = list(map(sCostoMecia, products["productos"]))
    # importe
 
    importe = lambda x: {**x, 'costoTotal': {**x['costoTotal'], 'importe': round(obtenerImporteIndividua(product=x),2)}}
    products['productos'] = list(map(importe, products["productos"]))

    #total importe
    totales_importe = round(sum(map(lambda x: x["costoTotal"]["importe"], products["productos"])),2)
    products['totales']["importe"] = totales_importe

    return products

#############################################################################################################################################################################
# Propuestas de costo de venta
#############################################################################################################################################################################
def ValorenVenta(product: dict,level: str,  porcentajeIVA: float):
    precioVentaPropuesto = product[level]['precioVentaPropuesto']

    porcentajeGanancia = ((precioVentaPropuesto * product['costoTotal']['CostoFinal'])/100) 
    IVA = precioVentaPropuesto*porcentajeIVA/100
    precioFinalIVA = porcentajeGanancia + IVA

    infoVenta = {"precioVentaPropuesto": precioVentaPropuesto,
                 "porcentajeGanancia": round(porcentajeGanancia, 2),
                 "porcentajeIVA": porcentajeIVA,
                 "IVA": IVA,
                 "precioFinalIVA":round(precioFinalIVA, 2)
                 }
    return infoVenta

def ActualizarPrecios(payments:dict, products:dict):
    porcentajeIVA = payments['tipoCambio']['globales']['porcentajeIVA']
    importe = lambda x: {**x, 'B2': ValorenVenta(product=x,level='B2', porcentajeIVA=porcentajeIVA)}
    products['productos'] = list(map(importe, products["productos"]))

    importe = lambda x: {**x, 'propuestaPropia': ValorenVenta(product=x,level='propuestaPropia', porcentajeIVA=porcentajeIVA)}
    products['productos'] = list(map(importe, products["productos"]))

    importe = lambda x: {**x, 'propuestaSuperior': ValorenVenta(product=x,level='propuestaSuperior', porcentajeIVA=porcentajeIVA)}
    products['productos'] = list(map(importe, products["productos"]))
    return products




#############################################################################################################################################################################
# Proceso
#############################################################################################################################################################################
print("*"*150)
with open('/home/PedroSci/eCommerce/DB_examples/rentabilidad_input.json', 'r') as f:
    rentabilidad =  json.loads(f.read())

# print(products) 
def pipelineCompleto(rentabilidad:dict):
    payments, products = extraerInformacion(rentabilidad=rentabilidad)
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
    #Paso 9. Obtener costos subtotales de producto
    products = obtenerSubtotal(payments=payments ,products=products)
    #paso 10. Obtener las prevalidaciones y DTA.
    products = obtenerA7(payments=payments ,products=products)
    #paso 11. Obtener IGI 
    products = obtenerA8(payments=payments ,products=products)
    #paso 12. Obtener el importe IVA
    products = obtenerA9(payments=payments ,products=products)
    #paso 13 obtener Costo Total
    products = obtenerCostoTotal(payments=payments ,products=products)
    #paso 13 actualizar con los precios
    products = ActualizarPrecios(payments=payments ,products=products)

    return products