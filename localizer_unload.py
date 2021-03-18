from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Updates the stored Robot's location in a db.
@app.route('/update_location', methods=['GET', 'POST'])
def update_location():
	position = request.get_json()['position']
	pos_db = open("pos_unloader.txt", "w")
	pos_db.write(str(position))

	return jsonify({"msg": "Localization Successful!"})

# Returns the Robot's location to the Unloader Componnent
@app.route('/get_location')
def get_location():
	pos_db = open("pos_unloader.txt", "r")
	str_pos = pos_db.readline()

	return jsonify({"position": str_pos})

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5001)