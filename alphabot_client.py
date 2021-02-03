import requests
import time

class ABclient:
	def __init__(self, role):
		self.role = role # 0 for loading, 1 for unloading
		self.curr_pos = 0 # AlphaBots starting position 
		inv_db = open("inv.txt", "r")
		self.end_pos = len(inv_db.readlines()) - 1 # find length of factory floor path
		inv_db.close

	def move(self, mission):

		""" Moves AlphaBot to the next position """

		print("Mission:", mission)

		# Invoke Unload Slice
		res = requests.post('http://localhost:5002/unload', json={"position": self.curr_pos})

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

		return next_pos
		

	def actuate(self, next_pos):
		""" Actually move AlphaBot to next position """

		""" input code here to actually actuate alphabot """

		self.curr_pos = next_pos
		time.sleep(2) # simulate AlphaBot movement duration

	def updateLocalizer(self, curr_pos):

		""" Invokes the Localizer Component in the respective Slice """

		res = requests.post('http://localhost:5001/', json={"position": curr_pos})
		if res.ok:
			print(res.json()['msg'])

	def getMission(self):

		""" Invokes the Mission Planner Component in the respective Slice """

		res = requests.get('http://localhost:5000/mission')
		if res.ok:
			return res.json()['mission']

	def inventoryFullyUnloaded(self, curr_pos):

		""" Invokes CSC to notify Inventory Loader Slice """

		print('Inventory in position', curr_pos, 'reached zero. Please Load.')
		self.updateLocalizer(curr_pos)


	def inventoryFullyLoaded(self):

		""" Invokes CSC to notify Inventory Unloader Slice """

if __name__ == '__main__':
	ab = ABclient(1)
	mission = ab.getMission()
	while(1): # move endlessly
		ab.move(mission)
		if (ab.curr_pos == 0): # if alphabot is back to base
			mission = ab.getMission()