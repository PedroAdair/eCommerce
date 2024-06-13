

| Funcion              | Params                                           |  KPI         |
|----------------------|--------------------------------------------------|--------------|
| consultaLicitaciones | (initial_date:str, end_date:str)                 | Licitaciones |
| gastoAcumuladoChat   | (concepto:str, initial_date: str, end_date:str)  | Rentabilidad |
| consultaInventario  | ()                                               | Inventario   |



## gastoAcumuladoChat

{
    "function": "gastoAcumuladoChat",
    "parameters": {
        "concepto": "flete",
        "initial_date":"02-05-2024",
        "end_date": "02-06-2024"
    }
}

"El gasto acumulado por el concepto de flete en el periodo que comprende del 02-05-2024 al 02-06-2024 es de 382,121.00 "

## consultaLicitaciones
{
    "function": "consultaLicitaciones",
    "parameters": {
        "initial_date":"02-05-2024",
        "end_date": "02-06-2024"
    }
}

Gener aun json con la estructura d euna lista de diccionarios con las llaves "_id" y "cantidadTotal". A continuacion se ve un ejemplo transformadoa  un df

|_id	                                |cantidadTotal |
|---------------------------------------|--------------|
|LUST RING vibrating cock and ballring	       | 360   |
|RUNNING WILD cock ballring W-taper plug	   | 100   |
|DOUBLE RIDER PRO Strapless Strap-On Vibrator  |320    |
|ENHANCER - ripple sleeve	                   | 80    |
|UTOPIA See- through stroker	               |  4    |
|ENHANCER - 7X Beads Sleeve	                   |  334  |
|EXTENDER - penis sleeve	                   |  360  |


## consultaInventario

{
    "function": "consultaInventario",
    "parameters": {
    }
}

|_id	                        | Total |
|-------------------------------|-------|
|Universal Pack	                | 500   |
|Caesarean Pack	                | 200   |
|Knee Arthscopy Pack	        | 100   |
|Cholecystomy Lparoscopy Pack	| 100   |
|Surgical Uniform	            | 15000 |
|Cystocopy Pack	                | 100   |
|Yellow Nursery Gown	        | 10000 |
|Shoulder Arthrscopy Pack	    | 100   |
|General Orthopedic Pack	    | 200   |
|Surgical Gown	                | 30000 |
|Delivery Pack	                | 100   |