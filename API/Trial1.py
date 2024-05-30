import json
from excelRentabilidad import *
#############
#input: un diccionario en forma de archivo json
#############

with open('DB_examples/inputRentabilidad.json', "r") as f:
    input = json.load(f)


#registrar un producto

producto1 = Producto(infoProduct=input['productos'][0])

datosPedimiento = producto1.getDatosPedimiento()

#registra los pagis asociados 

pagos = tipoCambio()

pagos.nuevoPago(informacion=input['tipoCambio']['historial'][0])
pagos.nuevoPago(informacion=input['tipoCambio']['historial'][1])
pagos.nuevoPago(informacion=input['tipoCambio']['historial'][2])



##A1 
a1 = producto1.getA1(tipoCambio=pagos.acumuladosGlobales()['tipoCambio'])
print(a1)