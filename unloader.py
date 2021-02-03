from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/unload', methods=['GET', 'POST'])
def unload():
	position = request.get_json()['position']
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
		print('Inventory fully undloaded. CSC to notify load Slice...')
		time.sleep(3)
		print('Loaded Successfully.')
		inv[position] = 3
	# update inv.db
	print("Inventory after:", inv)
	inv_db = open("inv.txt", "w")
	str_inv = [(str(i) + "\n") for i in inv] # back to strings for writing
	inv_db.writelines(str_inv)
	inv_db.close

	inv_db = open("inv.txt", "r") # weird bug fix (that blanks the file) TODO: check

	return 'Load Successful!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5002)