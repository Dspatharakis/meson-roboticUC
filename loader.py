from flask import Flask, request, jsonify
import threading
import requests
import time

app = Flask(__name__)

@app.route('/load', methods=['GET', 'POST'])
def load():
	position = request.get_json()['inv_position']
	th = threading.Thread(target=threadLoad(position))
	th.start()

	return jsonify({"msg": "AlphaBot en route to Load Position..."})

def threadLoad(position):
	time.sleep(10)
	requests.post('http://localhost:5002/update_inventory', json={"inv_position": position, "new_inv": 3})
	print("Load Finished in positition " + str(position))

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5003)