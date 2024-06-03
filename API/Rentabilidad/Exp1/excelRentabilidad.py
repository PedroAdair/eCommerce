from pymongo import MongoClient
import pymongo
from bson import ObjectId
import pandas as pd
from dotenv import load_dotenv
load_dotenv('venv/.env')
import os



#### Se crea una clase para esto
class tipoCambio:
    def __init__(self) -> None:
        self.historial = list()
        pass
    
    def nuevoPago(self, informacion:dict):
        infoPago = {"nombre": informacion["nombre"],
         "concepto": informacion["concepto"],
         "tipoCambio": informacion["tipoCambio"],
         "dolares":   informacion["dolares"]}
        self.historial.append(infoPago)
        return  infoPago
    
    def acumuladosGlobales(self):
        
        tipoCambio = sum(map(lambda x: x['tipoCambio'], self.historial)) / len(self.historial)
        totalDolares = sum(map(lambda x: x['dolares'], self.historial)) 
        globales = {
            'tipoCambio':round(tipoCambio,3),
            'totalDolares': totalDolares,
            'monedaNacional': round(tipoCambio*totalDolares)
        }
        return globales

class Producto():
    def __init__(self, 
                 infoProduct:dict):
        self.informacionGeneral = infoProduct['informacionGeneral']
        self.datosPedimiento    = infoProduct['datosPedimiento']
        
        self.A1                 = infoProduct['A1'] 
        self.A2                 = infoProduct['A2'] 
        self.A3                 = infoProduct['A3'] 
        self.A4                 = infoProduct['A4'] 
        self.A5                 = infoProduct['A5'] 
        self.A6                 = infoProduct['A6'] 
        self.A7                 = infoProduct['A7']
        self.A8                 = infoProduct['A8'] 
        self.A9                 = infoProduct['A9'] 

        self.B1                 = infoProduct['B1']
        self.B2                 = infoProduct['B2'] 
        self.propuestaPropia    = infoProduct['propuestaPropia']
        self.propuestaSuperior  = infoProduct['propuestaSuperior']
        
        self.costoTotal         = infoProduct['costoTotal']

    def getDatosPedimiento(self)->dict:
        """
        Se obtiene la informacion de la seccion de datos Pedimiento
    
        """
        importeMNAduana = self.datosPedimiento['importeMNAduana']
        flete           = self.datosPedimiento['flete']
        unidades        = self.datosPedimiento['unidades']

        total = importeMNAduana + flete
        costoUnitario = total/unidades
        
        datosPedimientoOutput = {"total": total,
                                "costoUnitario": costoUnitario
                                }
        return datosPedimientoOutput
    
    def getA1(self, tipoCambio)->dict:
        unidades         = self.datosPedimiento['unidades']
        costoUnitarioUSD = self.A1['costoUnitarioUSD']
        # pagos.acumuladosGlobales()['tipoCambio']  
        importeUSD = unidades*costoUnitarioUSD
        importeMN = importeUSD*tipoCambio
        A1_output = {
            "importeUSD": importeUSD,
            "importeMN": round(importeMN,2),
            "costoUnitarioMN": round(importeMN/unidades,2)
        }
        return A1_output

