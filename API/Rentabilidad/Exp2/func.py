from pymongo import MongoClient
import pymongo
from bson import ObjectId
import pandas as pd
from dotenv import load_dotenv
load_dotenv('venv/.env')
import os



class Producto():
    def __init__(self,infoProduct:dict):
        self.informacionGeneral = infoProduct['informacionGeneral']
        self.datosPedimiento    = infoProduct['datosPedimiento']
        self.A1                 = infoProduct['A1'] 

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
    
    def getA1(self)->dict:
        unidades         = self.datosPedimiento['unidades']
        costoUnitarioUSD = self.A1['costoUnitarioUSD']
        # pagos.acumuladosGlobales()['tipoCambio']  
        importeUSD = unidades*costoUnitarioUSD
        A1_output = {
            "importeUSD": importeUSD
        }
        return A1_output

class Totales():

    def __init__(self) -> None:
        pass
    
    