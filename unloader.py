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

	# Remove one object from the inventory if available
	if (inv[position] > 0):
		print('Removing one item...')
		inv[position] -= 1

		# Update inv.db
		print("Inventory after:", inv)
		inv_db = open("inv.txt", "w")
		str_inv = [(str(i) + "\n") for i in inv] # back to strings for writing
		inv_db.writelines(str_inv)
		inv_db.close

		inv_db = open("inv.txt", "r") # weird bug fix (that blanks the file) TODO: check

	else:
		print('Inventory fully undloaded.') 
		
		print('Notifying Mission Planner to skip position', position, 'in next mission, until loaded.')
		requests.post('http://localhost:5000/invalidate', json={"inv_position": position})

		print('CSC to notify Load Slice...')
		res = requests.post('http://localhost:5003/load', json={"inv_position": position})
		print(res.json()['msg'])

	return jsonify({"msg": "Unload Successful!"})

# Load Component from respective Slice calls this function to update the db with
# the new remaining inventory.
@app.route('/update_inventory', methods=['GET', 'POST'])
def update_inventory():
	json = request.get_json()
	position = json['inv_position']
	new_inv = json['new_inv']
	print(json)
	inv_db = open("inv.txt", "w")
	# inv_db.seek(0) # fix bug with open file, TODO: probably somehow connects with the bug above
	str_inv = inv_db.readlines()
	# print(str_inv)
	str_inv[position] = str(new_inv) + '\n'
	print(str_inv)
	inv_db.writelines(str_inv)
	inv_db.close

	# Invoke mission planner to validate the position.
	requests.post('http://localhost:5000/validate', json={"vld_position": position})
	print("Successfully updated inventory and validated position " + str(position))

	return jsonify({"msg": "Successfully updated inventory and validated position " + str(position)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5002)