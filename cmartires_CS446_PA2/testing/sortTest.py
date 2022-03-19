#practice with python

# class Car:
# 	def __init__(self, make, model, coolness):
# 		self.make = make
# 		self.model = model
# 		self.coolness = coolness
	
# 	def __repr__(self):
# 		return "Make: " + self.make + " Model: " + self.model + " Coolness: " + str(self.coolness)






class Process:
	def __init__(self, PID, arrivalTime, burstTime, priority):
		self.PID = PID
		self.arrivalTime = arrivalTime
		self.burstTime = burstTime
		self.priority = priority
	
	def __repr__(self):
		return '[' + str(self.PID) + ', ' + str(self.arrivalTime) + ', ' + str(self.burstTime) + ', ' + str(self.priority) + ']'

def main():
	# dreamCars = [Car("BMW", "E30", 10), Car("Datsun", "240z", 8.5), Car("Aston Martin", "DBS Superleggera", 9)]
	
	# print('Unsorted')
	# print(dreamCars)

	# sortedList = sorted(dreamCars, key = lambda x: x.coolness)
	# print('\nSorted')
	# print(sortedList)

	batchFile = open('pa2_batchfile.txt', 'r')
	data = batchFile.readlines()
	batchFile.close()

#-------start of function----passing in 'data'---#
	#print(len(data))
	#print(data)

	processes = []

	for x in data:
		tokens = x.split(', ')
		tokens[3] = tokens[3].replace('\n', '')
		#print(tokens)
		#print(tokens[3])

		processes.append(Process(int(tokens[0]), int(tokens[1]), int(tokens[2]), int(tokens[3])))

	print(processes)
	sortedProcesses = sorted(processes, key = lambda z: z.priority)
	print(sortedProcesses)

	for y in processes:
		print(y.arrivalTime)
	#sortedList = sorted(data)
	#print(sortedList)
	


if __name__ == "__main__":
	main()