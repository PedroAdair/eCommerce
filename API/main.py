from flask import Flask, jsonify , request
from flask_cors import CORS
import yaml 
from recepcionProductos import *
from rentabilidad import * 
from KPIRentabilidad import *
from KPILicitaciones import *
from KPIInventario import * 
with open('config.yaml', "r") as f:
    config = yaml.safe_load(f)

app = Flask(__name__)
CORS(app)

@app.route("/first_get")
def root():
    return 'que aces',201 


@app.route('/KPI', methods=['POST'])
def FirstPost():
    data = request.get_json()
    print(data)
    result = eval(data['function'])(*data['parameters'].values())
    print(result)
    return jsonify(result),200

@app.route('/rentabilidad', methods=['POST'])
def getrentabilidad():
    data = request.get_json()
    result = pipelineCompleto(rentabilidad=data)
    print(result)
    return jsonify(result),200

if __name__ == '__main__':
    app.run(debug=True, host = '192.168.100.11', port=config['port']) #config['port']4100 