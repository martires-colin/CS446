#Program Name: batchSchedulingComparison.py
#Author: Colin Martires
#Purpose: Programming Assignment 2

#Compare and contrast the two algorithms. Explain where each would be
#appropriate and any possible tradeoffs in implementation or process execution

import sys
import os.path

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
	#print(data)		#check data read from file

	#execute sorting algorithms
	if(sys.argv[2] == 'FCFS'):
		#FCFS stuff
		print('You\'ve chosen FCFS')
	elif(sys.argv[2] == 'ShortestFirst'):
		#ShortestFirst stuff
		print('You\'ve chosen ShortestFirst')
	elif(sys.argv[2] == 'Priority'):
		#Priority stuff
		print('You\'ve chosen Priority')





if __name__ == '__main__':
	main()