from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def notify_pp_and_iu():
    content = request.json
    position = content['position']

    print('Notifying Mission Planner to skip position', position, 'in next mission, until loaded.')
    res = requests.post('http://localhost:5000/invalidate', json={"inv_position": position})

    print('Notifying Inventory Unloader to initiate CSC actions to load position', content['position'], '.')
    
    return jsonify({"msg": "Successfully invalidated position: " + str(position)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)