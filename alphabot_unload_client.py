import requests
import time

# A client that turns an AlphaBot into an Unload Agent.
# To be deployed in the Alphabot
class UnloadClient:
	def __init__(self):
		self.curr_pos = 0 # AlphaBots starting position 
		self.end_pos = 2 # find length of factory floor path

	def move(self, mission):
		""" Moves AlphaBot to the next position """
		print("Mission:", mission)

		# First invoke the Unload Component
		self.unload()

		# Then, move to next *valid* position
		if ((self.curr_pos + 1) > self.end_pos): # if last position of path is reached
			next_pos = 0 # move back to base
		else:
			next_pos = self.curr_pos + 1
			while(mission[next_pos] == 0):
				if (next_pos + 1 > self.end_pos):
					next_pos = 0
					break
				else:
					next_pos += 1
		self.actuate(next_pos)
		self.updateLocalizer()

		return next_pos
	
	def actuate(self, next_pos):
		""" Actually move AlphaBot to next position """
		""" TODO: input code here to actually actuate alphabot """
		self.curr_pos = next_pos
		print("Moving to next position: " + str(next_pos))
		time.sleep(2) # simulate AlphaBot movement duration

	def unload(self):
		""" Invokes the Unloader Component in the respective Slice """
		res = requests.post('http://localhost:5002/unload', json={"position": self.curr_pos})
		if res.ok:
			print(res.json()['msg'])

	def updateLocalizer(self):
		""" Invokes the Localizer Component in the respective Slice """
		res = requests.post('http://localhost:5001/update_location', json={"position": self.curr_pos})
		if res.ok:
			print(res.json()['msg'])

	def getMission(self):
		""" Invokes the Mission Planner Component in the respective Slice """
		res = requests.get('http://localhost:5000/get_mission')
		if res.ok:
			return res.json()['mission']

if __name__ == '__main__':
	ab = UnloadClient()
	mission = ab.getMission()
	while(1): # move endlessly
		ab.move(mission)
		if (ab.curr_pos == 0): # if alphabot is back to base
			mission = ab.getMission()
		input("Press Enter to continue...") # for debugging purposes
