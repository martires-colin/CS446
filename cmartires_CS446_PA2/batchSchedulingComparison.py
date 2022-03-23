#Program Name: batchSchedulingComparison.py
#Author: Colin Martires
#Purpose: Programming Assignment 2

#Compare and contrast the three algorithms. Explain where each would be
#appropriate and any possible tradeoffs in implementation or process execution

import sys
import os.path
import operator
from collections import deque

#class to store proces information
class Process:
	def __init__(self, PID, arrivalTime, burstTime, priority):
		self.PID = PID
		self.arrivalTime = arrivalTime
		self.burstTime = burstTime
		self.priority = priority
		self.jobTime = burstTime
	
	def __repr__(self):
		return '[' + str(self.PID) + ', ' + str(self.arrivalTime) + ', ' + str(self.burstTime) + ', ' + str(self.priority) + ']'

def AverageTurnaround(processCompletionTimes, processArrivalTimes):
	processTurnaroundTimes = list(map(operator.sub, processCompletionTimes, processArrivalTimes))
	turnaroundTime = sum(processTurnaroundTimes)
	avgTurnaroundTime = turnaroundTime / len(processCompletionTimes)
	return avgTurnaroundTime, processTurnaroundTimes
	
def AverageWait(processTurnaroundTimes, processBurstTimes):
	processWaitTimes = list(map(operator.sub, processTurnaroundTimes, processBurstTimes))
	waitTime = sum(processWaitTimes)
	avgWaitTime = waitTime / len(processTurnaroundTimes)
	return avgWaitTime

def processBatchData(batchFileData):
	processList = []
	for x in batchFileData:
		tokens = x.split(', ')
		tokens[3] = tokens[3].replace('\n', '')
		processList.append(Process(int(tokens[0]), int(tokens[1]), int(tokens[2]), int(tokens[3])))
	return processList

def FirstComeFirstServedSort(batchFileData):
	processes = processBatchData(batchFileData)
	sortedProcesses = sorted(processes, key = lambda z: (z.arrivalTime, z.PID))
	
	PIDlist = []
	ArrivalTimeList = []
	BurstTimeList = []
	completionTimeList = []
	completionTime = 0
	for i in sortedProcesses:
		PIDlist.append(i.PID)
		ArrivalTimeList.append(i.arrivalTime)
		BurstTimeList.append(i.burstTime)
		completionTime += i.burstTime
		completionTimeList.append(completionTime)

	# print(sortedProcesses)
	# print(PIDlist)
	# print(completionTimeList)

	return PIDlist, completionTimeList, ArrivalTimeList, BurstTimeList

def ShortestJobFirstSort(batchFileData):
	processes = processBatchData(batchFileData)
	sortedProcesses = sorted(processes, key = lambda z: (z.arrivalTime, z.PID))

	readyQueue = deque()
	executionList = []
	numCompleted = 0
	time = 0
	prev = 0

	PIDlist = []
	ArrivalTimeList = []
	BurstTimeList = []
	completionTimeList = []
	while(numCompleted != len(sortedProcesses)):
		for x in sortedProcesses:			#insert processes that have arrived in ready queue
			if(x.arrivalTime == time):
				readyQueue.append(x)

		shortestBurst = min(readyQueue, key = lambda x: x.burstTime)
		currentProcess = shortestBurst

		if(currentProcess.PID != prev):
			PIDlist.append(currentProcess.PID)
		prev = shortestBurst.PID

		currentProcess.burstTime -= 1		#simulate process execution
		executionList.append(currentProcess)

		if(currentProcess.burstTime == 0):	#process has completed
			numCompleted += 1
			readyQueue.remove(currentProcess)
			ArrivalTimeList.append(currentProcess.arrivalTime)
			BurstTimeList.append(currentProcess.jobTime)
			completionTimeList.append(time + 1)

		time += 1

	# print(PIDlist)
	# print(ArrivalTimeList)
	# print(completionTimeList)
	# print(BurstTimeList)


	return PIDlist, completionTimeList, ArrivalTimeList, BurstTimeList

def PrioritySort(batchFileData):
	processes = processBatchData(batchFileData)
	sortedProcesses = sorted(processes, key = lambda z: (z.arrivalTime, z.priority, z.PID))
	
	PIDlist = []
	ArrivalTimeList = []
	BurstTimeList = []
	completionTimeList = []
	completionTime = 0
	for i in sortedProcesses:
		PIDlist.append(i.PID)
		ArrivalTimeList.append(i.arrivalTime)
		BurstTimeList.append(i.burstTime)
		completionTime += i.burstTime
		completionTimeList.append(completionTime)

	# print(sortedProcesses)
	# print(PIDlist)
	# print(completionTimeList)

	return PIDlist, completionTimeList, ArrivalTimeList, BurstTimeList

def main():

	#CHECK COMMAND LINE ARGUMENTS
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

	#READ FILE DATA
	batchFile = sys.argv[1]
	batchFile = open(sys.argv[1], 'r')
	data = batchFile.readlines()
	batchFile.close()

	#EXECUTE SORTING ALGORITHMS
	if(sys.argv[2] == 'FCFS'):
		PIDs, CompletionTimes, ArrivalTimes, BurstTimes = FirstComeFirstServedSort(data)
		
		avgTurnaroundTime, TurnaroundTimes = AverageTurnaround(CompletionTimes, ArrivalTimes)
		avgWaitTime = AverageWait(TurnaroundTimes, BurstTimes)

		# print('PIDs:',PIDs)								#checking results(remove after)
		# print('Completion Times:', CompletionTimes)		#checking results
		# print('Arrival Times:', ArrivalTimes)			#checking results
		# print('Burst Times:', BurstTimes)				#checking results
		# print('Turnaround Times:', TurnaroundTimes)		#checking results

		print('FCFS Sort Statistics:')
		print('PID ORDER OF EXECUTION')
		for i in PIDs:
			print(i)
		print('Average Process Turnaround Time: {:0.2f}'. format(avgTurnaroundTime))
		print('Average Process Wait Time: {:0.2f}'. format(avgWaitTime))

	elif(sys.argv[2] == 'ShortestFirst'):
		PIDs, CompletionTimes, ArrivalTimes, BurstTimes = ShortestJobFirstSort(data)

		avgTurnaroundTime, TurnaroundTimes = AverageTurnaround(CompletionTimes, ArrivalTimes)
		avgWaitTime = AverageWait(TurnaroundTimes, BurstTimes)
		
		# print('PIDs:',PIDs)								#checking results(remove after)
		# print('Completion Times:', CompletionTimes)		#checking results
		# print('Arrival Times:', ArrivalTimes)			#checking results
		# print('Burst Times:', BurstTimes)				#checking results
		# print('Turnaround Times:', TurnaroundTimes)		#checking results

		print('Shortest Job First Sort Statistics:')
		print('PID ORDER OF EXECUTION')
		for i in PIDs:
			print(i)
		print('Average Process Turnaround Time: {:0.2f}'. format(avgTurnaroundTime))
		print('Average Process Wait Time: {:0.2f}'. format(avgWaitTime))

	elif(sys.argv[2] == 'Priority'):
		PIDs, CompletionTimes, ArrivalTimes, BurstTimes = PrioritySort(data)
		
		avgTurnaroundTime, TurnaroundTimes = AverageTurnaround(CompletionTimes, ArrivalTimes)
		avgWaitTime = AverageWait(TurnaroundTimes, BurstTimes)

		# print('PIDs:',PIDs)								#checking results(remove after)
		# print('Completion Times:', CompletionTimes)		#checking results
		# print('Arrival Times:', ArrivalTimes)			#checking results
		# print('Burst Times:', BurstTimes)				#checking results
		# print('Turnaround Times:', TurnaroundTimes)		#checking results

		print('Priority Sort Statistics:')
		print('PID ORDER OF EXECUTION')
		for i in PIDs:
			print(i)
		print('Average Process Turnaround Time: {:0.2f}'. format(avgTurnaroundTime))
		print('Average Process Wait Time: {:0.2f}'. format(avgWaitTime))

if __name__ == '__main__':
	main()