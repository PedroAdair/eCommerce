import json
from func import *

with open('DB_examples/primerinputProductos.json', "r") as f:
    input = json.load(f)


#registrar un producto

producto1 = Producto(infoProduct=input['productos'][0])
producto2 = Producto(infoProduct=input['productos'][1])
producto3 = Producto(infoProduct=input['productos'][2])