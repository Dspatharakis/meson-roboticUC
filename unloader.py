from flask import Flask, request, jsonify
import time
import requests

app = Flask(__name__)

@app.route('/unload', methods=['GET', 'POST'])
def unload():
	position = int(requests.get('http://localhost:5001/get_location').json()['position'])
	inv_db = open("inv.txt", "r")
	str_inv = inv_db.readlines()
	inv = [int(i) for i in str_inv]
	print("Inventory before:", inv)
	print('Inventory in position', position, ':', inv[position])

	# remove one object from the inventory if available
	if (inv[position] > 0):
		print('Removing one item...')
		inv[position] -= 1
	else:
		# self.inventoryFullyUnloaded(self.curr_pos)
		print('Inventory fully undloaded.') 
		print('CSC to notify Load Slice...')
		time.sleep(3) # TODO: input code here to actually actuate invoke the Load Slice
		print('Notifying Mission Planner to skip position', position, 'in next mission, until loaded.')
		res = requests.post('http://localhost:5000/invalidate', json={"inv_position": position})
		# print('Loaded Successfully.')
		# inv[position] = 3

	# update inv.db
	print("Inventory after:", inv)
	inv_db = open("inv.txt", "w")
	str_inv = [(str(i) + "\n") for i in inv] # back to strings for writing
	inv_db.writelines(str_inv)
	inv_db.close

	inv_db = open("inv.txt", "r") # weird bug fix (that blanks the file) TODO: check

	return jsonify({"msg": "Unload Successful!"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5002)