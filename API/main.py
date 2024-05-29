from flask import Flask, jsonify , request
from flask_cors import CORS
import yaml 

with open('config.yaml', "r") as f:
    config = yaml.safe_load(f)

app = Flask(__name__)
CORS(app)

@app.route('/KPI', methods=['POST'])

def FirstPost():
    data = request.get_json()
    # result = eval(data['function'])(*data['parameters'].values())
    # print(result)
    return jsonify(data),200

if __name__ == '__main__':
    app.run(debug=True, host = '192.168.100.11', port=config['port']) #config['port']4100 