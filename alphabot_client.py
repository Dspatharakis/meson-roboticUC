import requests
import time

class ABclient:
	def __init__(self, role):
		self.role = role # 0 for loading, 1 for unloading
		self.curr_pos = 0 # AlphaBots starting position 
		inv_db = open("inv.txt", "r")
		self.end_pos = len(inv_db.readlines()) - 1 # find length of factory floor path
		inv_db.close

	def move(self):
		""" Moves AlphaBot to the next position """
		# First, perfom load/unload on current position
		if (self.role == 1): # unloading
			# read inv.db and convert to integers
			inv_db = open("inv.txt", "r")
			str_inv = inv_db.readlines()
			inv = [int(i) for i in str_inv]
			print(inv)
			print('Inventory in position', self.curr_pos, ':', inv[self.curr_pos])

			# remove one object from the inventory if available
			if (inv[self.curr_pos] > 0):
				print('Removing one item...')
				inv[self.curr_pos] -= 1
			else:
				self.inventoryFullyUnloaded(self.curr_pos)
			# update inv.db
			print(inv)
			inv_db = open("inv.txt", "w")
			str_inv = [(str(i) + "\n") for i in inv] # back to strings for writing
			inv_db.writelines(str_inv)
			inv_db.close
		else: # loading
			print('Loading')

		# Then, move to next position
		if ((self.curr_pos + 1) > self.end_pos): # if last position of path is reached
			next_pos = 0 # move back to base
		else:
			next_pos = self.curr_pos + 1
		self.actuate(next_pos)
		

	def actuate(self, next_pos):
		""" Actually move AlphaBot to next position """

		""" input code here to actually actuate alphabot """

		self.curr_pos = next_pos

	def updateLocalizer(self, curr_pos):
		""" Invokes the Localizer Component in the respective Slice """
		res = requests.post('http://localhost:5000/', json={"position":curr_pos})

	def inventoryFullyUnloaded(self, curr_pos):
		""" Invokes CSC to notify Inventory Loader slice """
		print('Inventory in position', curr_pos, 'reached zero. Please Load.')
		self.updateLocalizer(curr_pos)

	def inventoryFullyLoaded(self):
		""" Invokes CSC to notify Inventory Unloader slice """

if __name__ == '__main__':
	ab = ABclient(1)
	while(1): # move endlessly
		ab.move()
		time.sleep(2) # simulate AlphaBot movement duration

# res = requests.post('http://127.0.0.1:5000/api/add_message/1234', json={"mytext":"lalala"})
# if res.ok:
#     print(res.json())