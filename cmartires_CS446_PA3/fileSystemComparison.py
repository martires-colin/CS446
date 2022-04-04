#Program Name: fileSystemComparison.py
#Author: Colin Martires
#Purpose: Programming Assignment 3
#This program will compare and contrast single-level and heirarchical file
#directories. The program will determine the size difference as well as the
#traversal time between the two types of directories.

# COMPARE THE THINGIES

# To Do
# move files into directories in hierarchicalRoot

import os
import shutil

def generateFiles(path, numOfFiles, start):
	os.chdir(path)
	for i in range(start, numOfFiles):
		with open('file' + str(i + 1) + '.txt', 'w'):
			pass

def createDirectories(path, numDirectories):
	os.chdir(path)
	offset = 0
	fileCtr = 10
	start = 0
	for i in range(numDirectories):
		directoryName = 'files' + (str)(offset + 1) + '-' + (str)(offset + 10) 
		os.makedirs(directoryName, exist_ok=True)
		os.chdir(directoryName)
		generateFiles(path + '/' + directoryName, fileCtr, start)
		offset += 10
		fileCtr += 10
		start += 10
		os.chdir(path)

def moveToDirectory():
	pass

def main():

	os.makedirs('/home/cmartires/singleRoot', exist_ok=True)			#create singleRoot directory
	os.makedirs('/home/cmartires/hierarchicalRoot', exist_ok=True)		#create hierarchicalRoot directory

	generateFiles('/home/cmartires/singleRoot', 100, 0)					#generate 100 files in singleRoot
	createDirectories('/home/cmartires/hierarchicalRoot', 10)			#generate directories?files within hierarchicalRoot


if __name__ == '__main__':
	main()