#Program Name: batchSchedulingComparison.py
#Author: Colin Martires
#Purpose: Programming Assignment 2

#Compare and contrast the two algorithms. Explain where each would be
#appropriate and any possible tradeoffs in implementation or process execution

import sys
import os.path
import operator

#class to store proces information
class Process:
	def __init__(self, PID, arrivalTime, burstTime, priority):
		self.PID = PID
		self.arrivalTime = arrivalTime
		self.burstTime = burstTime
		self.priority = priority
	
	def __repr__(self):
		return '[' + str(self.PID) + ', ' + str(self.arrivalTime) + ', ' + str(self.burstTime) + ', ' + str(self.priority) + ']'

def AverageTurnaround(processCompletionTimes, processArrivalTimes):
	processTurnaroundTimes = list(map(operator.sub, processCompletionTimes, processArrivalTimes))
	turnaroundTime = sum(processTurnaroundTimes)
	avgTurnaroundTime = turnaroundTime / len(processCompletionTimes)
	return avgTurnaroundTime, processTurnaroundTimes
	
def AverageWait(processTurnaroundTimes, processBurstTime):
	processWaitTimes = list(map(operator.sub, processTurnaroundTimes, processBurstTime))
	waitTime = sum(processWaitTimes)
	avgWaitTime = waitTime / len(processTurnaroundTimes)
	return avgWaitTime

def FirstComeFirstServedSort(batchFileData):
	processes = []
	for x in batchFileData:
		tokens = x.split(', ')
		tokens[3] = tokens[3].replace('\n', '')
		processes.append(Process(int(tokens[0]), int(tokens[1]), int(tokens[2]), int(tokens[3])))
	
	#print(processes)
	sortedProcesses = sorted(processes, key = lambda z: (z.arrivalTime, z.PID))
	
	PIDlist = []
	ArrivalTimeList = []
	BurstTimeList = []
	for i in sortedProcesses:
		PIDlist.append(i.PID)
		ArrivalTimeList.append(i.arrivalTime)
		BurstTimeList.append(i.burstTime)

	completionTime = 0
	completionTimeList = []
	for y in sortedProcesses:
		completionTime += y.burstTime
		completionTimeList.append(completionTime)

	# print(sortedProcesses)
	# print(PIDlist)
	# print(completionTimeList)

	return PIDlist, completionTimeList, ArrivalTimeList, BurstTimeList



def main():

	#check for correct number of arguments
	if(len(sys.argv) != 3):
		print('[ERROR]: Incorrect number of arguments')
		print('usage: batchSchedulingComparison.py <batchFile> <sortType>')
		return 0
	elif(os.path.exists(sys.argv[1]) == 0):
		print('[ERROR]: File Not Found')
		return 0
	elif((sys.argv[2] != 'FCFS') and (sys.argv[2] != 'ShortestFirst') and (sys.argv[2] != 'Priority')):
		print('[Error]: Algorithm not recognized')
		print('Algorithm Options: FCFS, ShortestFirst, Priority')
		return 0

	#read contents of batch file
	batchFile = sys.argv[1]
	batchFile = open(sys.argv[1], 'r')
	data = batchFile.readlines()
	batchFile.close()
	#print(data)		#check data read from file				PID, Arrival Time, Burst Time, Priority

	#execute sorting algorithms
	if(sys.argv[2] == 'FCFS'):
		PIDs, CompletionTimes, ArrivalTimes, BurstTimes = FirstComeFirstServedSort(data)	#call FirstComeFirstServedSort
		
		avgTurnaroundTime, TurnaroundTimes = AverageTurnaround(CompletionTimes, ArrivalTimes)
		avgWaitTime = AverageWait(TurnaroundTimes, BurstTimes)

		print('PIDs:',PIDs)								#checking results	
		print('Completion Times:', CompletionTimes)		#checking results
		print('Arrival Times:', ArrivalTimes)			#checking results
		print('Burst Times:', BurstTimes)				#checking results
		print('Turnaround Times:', TurnaroundTimes)		#checking results

		print('FCFS Sort Statistics:')
		print('PID ORDER OF EXECUTION')
		for i in PIDs:
			print(i)
		#print('Each Processes\'s Turnaround Time:', processTurnaroundTimes)
		print('Average Process Turnaround Time:', avgTurnaroundTime)
		print('Average Process Wait Time:', avgWaitTime)

	elif(sys.argv[2] == 'ShortestFirst'):
		#ShortestFirst stuff
		print('You\'ve chosen ShortestFirst')
	elif(sys.argv[2] == 'Priority'):
		#Priority stuff
		print('You\'ve chosen Priority')

if __name__ == '__main__':
	main()