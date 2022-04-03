#Program Name: fileSystemComparison.py
#Author: Colin Martires
#Purpose: Programming Assignment 3
#This program will compare and contrast single-level and heirarchical file
#directories. The program will determine the size difference as well as the
#traversal time between the two types of directories.

# To Do
# move files into directories in hierarchicalRoot

import os
import shutil

def generateFiles(path, numOfFiles):
	os.chdir(path)
	ctr = 0
	for i in range(numOfFiles):
		with open('file' + str(i + 1) + '.txt', 'w'):
			pass
		ctr += 1
	return ctr

def createDirectories(path, numDirectories):
	os.chdir(path)
	offset = 0
	for i in range(numDirectories):
		directoryName = 'files' + (str)(offset + 1) + '-' + (str)(offset + 10) 
		os.makedirs(directoryName, exist_ok=True)
		offset += 10

def moveToDirectory():
	pass

def main():

	os.makedirs('/home/cmartires/singleRoot', exist_ok=True)			#create singleRoot directory
	os.makedirs('/home/cmartires/hierarchicalRoot', exist_ok=True)		#create hierarchicalRoot directory

	numSRfiles = generateFiles('/home/cmartires/singleRoot', 100)		#generate 100 files in singleRoot
	numHRfiles = generateFiles('/home/cmartires/hierarchicalRoot', 100)	#generate 100 files in heirarchicalRoot
	createDirectories('/home/cmartires/hierarchicalRoot', 10)				#generate directories within hierarchicalRoot


if __name__ == '__main__':
	main()