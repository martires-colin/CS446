#practice with python

class Car:
	def __init__(self, make, model, coolness):
		self.make = make
		self.model = model
		self.coolness = coolness
	
	def __repr__(self):
		return "Make: " + self.make + " Model: " + self.model + " Coolness: " + str(self.coolness)

def main():
	dreamCars = [Car("BMW", "E30", 10), Car("Datsun", "240z", 8.5), Car("Aston Martin", "DBS Superleggera", 9)]
	
	print('Unsorted')
	print(dreamCars)

	sortedList = sorted(dreamCars, key = lambda x: x.coolness)
	print('\nSorted')
	print(sortedList)

if __name__ == "__main__":
	main()