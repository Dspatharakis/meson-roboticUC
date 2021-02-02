from flask import Flask, request, jsonify

app = Flask(__name__)

# Return the mission path based on inventory availability
# 1 - visiting, 0 - not visiting
@app.route('/mission')
def getMission():
    mission_f = open("mission.txt", "r")
    str_mission = mission_f.readlines()
    mission = [int(i) for i in str_mission]

    return jsonify({"mission": mission})

# Alter mission path based on inventory availability
# 1 - visiting, 0 - not visiting
@app.route('/invalidate', methods=['GET', 'POST'])
def invalidatePosition():
	content = request.json
	inv_position = content['inv_position']
	mission_f = open("mission.txt", "r")
	str_mission = mission_f.readlines()
	mission = [int(i) for i in str_mission]
	mission[inv_position] = 0

    # write mission back
	mission_f = open("mission.txt", "w")
	str_mission = [(str(i) + "\n") for i in mission] # back to strings for writing
	mission_f.writelines(str_mission)
	mission_f.close

	return "Successfully invalidated position: " + str(inv_position)

# Alter mission path based on inventory availability
# 1 - visiting, 0 - not visiting
@app.route('/validate', methods=['GET', 'POST'])
def validatePosition():
	content = request.json
	vld_position = content['vld_position']
	mission_f = open("mission.txt", "w")
	str_mission = mission_f.readlines()
	mission = [int(i) for i in str_mission]
	mission[vld_position] = 1

    # write mission back
	mission_f = open("mission.txt", "w")
	str_mission = [(str(i) + "\n") for i in mission] # back to strings for writing
	mission_f.writelines(str_mission)
	mission_f.close

	return "Successfully validated position: " + str(vld_position)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5000)
