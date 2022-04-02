#Program Name: fileSystemComparison.py
#Author: Colin Martires
#Purpose: Programming Assignment 3
#This program will compare and contrast single-level and heirarchical file
#directories. The program will determine the size difference as well as the
#traversal time between the two types of directories.

# To Do
# create directories in hierarchicalRoot

import os

def generateFiles(path, numOfFiles):
	os.chdir(path)
	ctr = 0
	for i in range(numOfFiles):
		with open('file' + str(i + 1) + '.txt', 'w'):
			pass
		ctr += 1
		# os.remove('file' + str(i + 1) + '.txt') #remove files
	# print('printed', ctr, 'files') #check total number of printed files
	return ctr

def moveToDirectory():


def main():
	numSRfiles = generateFiles('/home/cmartires/singleRoot', 100)		#generate 100 files in singleRoot
	numHRfiles = generateFiles('/home/cmartires/hierarchicalRoot', 100)		#generate 100 files in heirarchicalRoot

	


if __name__ == '__main__':
	main()