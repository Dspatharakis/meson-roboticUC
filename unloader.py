from flask import Flask, request, jsonify
import time
import requests
import csv 
app = Flask(__name__)

# Updates the db and invokes Mission Planner and Loader Component (CSC)
@app.route('/unload', methods=['GET', 'POST'])
def unload():
	position = int(requests.get('http://localhost:5001/get_location').json()['position'])
	inv_db = open("inv_unloader.txt", "r")
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
		inv_db = open("inv_unloader.txt", "w")
		str_inv = [(str(i) + "\n") for i in inv] # back to strings for writing
		inv_db.writelines(str_inv)
		inv_db.close

		inv_db = open("inv_unloader.txt", "r") # weird bug fix (that blanks the file) TODO: check

	else:
		print('Inventory fully undloaded.') 
		
		print('Notifying Mission Planner to skip position', position, 'in next mission, until loaded.')
		requests.post('http://localhost:5000/invalidate', json={"inv_position": position})

		print('CSC to notify Load Slice...')
		img = "./img/" + "1.jpg"
		files = {"file": open("./" + img, "rb")}
		transmission_time_start = time.time() 
		res = requests.post('http://localhost:5003/load_image', files=files)
		print(res.json()['msg'])
		res = requests.post('http://localhost:5003/load', json={"inv_position": position})
		print(res.json()['msg'])
		transmission_time = time.time() - transmission_time_start
		print ("Transmission time for CSC:" , transmission_time)
		filename = "./transmission_time.txt"
		with open(filename, 'a') as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			wr.writerow([round(transmission_time,5)])
	return jsonify({"msg": "Unload Successful!"})

# The Loader Component from respective Slice calls this function to update the db with
# the new remaining inventory.
@app.route('/update_inventory', methods=['GET', 'POST'])
def update_inventory():
	json = request.get_json()
	position = json['inv_position']
	new_inv = json['new_inv']

	inv_db = open("inv_unloader.txt", "r")
	str_inv = inv_db.readlines()
	inv = [int(i) for i in str_inv]

	inv_db = open("inv_unloader.txt", "w")
	str_inv = [(str(i) + "\n") for i in inv]
	str_inv[position] = str(new_inv) + '\n'
	inv_db.writelines(str_inv)
	inv_db.close

	inv_db = open("inv_unloader.txt", "r") # weird bug fix (that blanks the file) TODO: check

	# Invoke Mission Planner to validate the position.
	requests.post('http://localhost:5000/validate', json={"vld_position": position})
	print("Successfully updated inventory and validated position " + str(position))

	return jsonify({"msg": "Successfully updated inventory and validated position " + str(position)})

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5002)