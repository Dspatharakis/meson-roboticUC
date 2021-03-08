from flask import Flask, request, jsonify
import threading
import requests
import time

app = Flask(__name__)

# Invoked via CSC by the Unloader Component in order to send the Loader Robot
# to load the empty inventory.
@app.route('/load', methods=['GET', 'POST'])
def load():
	position = request.get_json()['inv_position']
	th = threading.Thread(target=threadLoad, args=(position,)) # simulates the asynchronus alphabot movement
	th.start()

	return jsonify({"msg": "AlphaBot en route to Load Position..."})

# Simulation of an Asynchronus Alphabot Movement towards the empty inventory position in order to reload.
def threadLoad(position):
	time.sleep(10) # simulate the time it takes to get to the empty position.
	requests.post('http://localhost:5002/update_inventory', json={"inv_position": position, "new_inv": 3})
	print("Load Finished in position " + str(position))

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5003)