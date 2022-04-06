# Program Name: fileSystemComparison.py
# Author: Colin Martires
# Purpose: Programming Assignment 3
# This program will compare and contrast single-level and heirarchical file
# directories. The program will determine the size difference as well as the
# traversal time between the two types of directories.

# -----singleLevelFiles.txt vs hierarchicalFiles.txt-----
# Both text files contain 100 files with a size of 0 bytes. The difference is
# that in hierarchicalRoot, the files are sorted into 10 subdirectories each containing
# 10 of the 100 total files generated. This means that when printing the file data to
# hierarchicalFiles.txt, the 10 subdirectories will be included. singleLevelFiles.txt
# contains 100 files of size 0 bytes while hierarchicalFiles.txt contains 100 files of
# size 0 bytes and 10 files of size 4096 bytes. 

# -----How can we implement something similar to a hierarchical file system?-----




import os
import time

def generateFiles(path, numOfFiles, start):
	origin = os.getcwd()
	os.chdir(path)
	for i in range(start, numOfFiles):
		with open('file' + str(i + 1) + '.txt', 'w'):
			pass
	os.chdir(origin)

def createDirectories(path, numDirectories):
	origin = os.getcwd()
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
	os.chdir(origin)

def traverseDirectory(filePath):
	dirInfo = {}

	dirs = next(os.walk(filePath))[1]
	for dirName in dirs:
		fileSize = os.path.getsize(filePath + '/' + dirName)
		dirInfo[dirName] = fileSize
	
		files = next(os.walk(filePath + '/' + dirName))[2]
		for fileName in files:
			fileSize = os.path.getsize(filePath + '/' + dirName + '/' + fileName)
			dirInfo[fileName] = fileSize

	files = next(os.walk(filePath))[2]
	for fileName in files:
		fileSize = os.path.getsize(filePath + '/' + fileName)
		dirInfo[fileName] = fileSize

	return dirInfo

def writeDataFile(data, fileName, destination):
	origin = os.getcwd()
	os.chdir(destination)
	f = open(fileName, "w")
	for key, value in data.items():
		f.write('File Name: %s\nFile Size: %s bytes\n\n' % (key,value))
	f.close()
	os.chdir(origin)
	return len(data)

def calculateAvgSize(data):
	size = 0
	for key, value in data.items():
		size += value
	return size / len(data)

def main():

	os.makedirs('/home/cmartires/singleRoot', exist_ok=True)			#create singleRoot directory
	os.makedirs('/home/cmartires/hierarchicalRoot', exist_ok=True)		#create hierarchicalRoot directory

	generateFiles('/home/cmartires/singleRoot', 100, 0)					#generate 100 files in singleRoot
	createDirectories('/home/cmartires/hierarchicalRoot', 10)			#generate directories and files within hierarchicalRoot

	timeStartSR = time.time()											#start timer for singleRoot traversal
	SRdata = traverseDirectory('/home/cmartires/singleRoot')			#traverse singleRoot
	timeEndSR = time.time()												#end timer for singleRoot traversal
	
	timeStartHR = time.time()											#start timer for hierarchicalRoot traversal
	HRdata = traverseDirectory('/home/cmartires/hierarchicalRoot')		#traverse hierarchicalRoot
	timeEndHR = time.time()												#end timer for hierarchical traversal

	numSRfiles = writeDataFile(SRdata, 'singleLevelFiles.txt', '/home/cmartires/singleRoot')		#write data to file					#write files with directory info
	numHRfiles = writeDataFile(HRdata, 'hierarchicalFiles.txt', '/home/cmartires/hierarchicalRoot')

	avgSizeSR = calculateAvgSize(SRdata)								#calculate average file size
	avgSizeHR = calculateAvgSize(HRdata)

	traversalTimeSR = (timeEndSR - timeStartSR) * 1000					#calculate traversal time
	traversalTimeHR = (timeEndHR - timeStartHR) * 1000

	print('singleRoot Statistics:')
	print('Number of Files:', numSRfiles)
	print('Average File Size: %0.2f' % avgSizeSR)
	print('Traversal Time: %0.2f ms' % traversalTimeSR)
	
	print('\nhierarchicalRoot Statistics:')
	print('Number of Files:', numHRfiles)
	print('Average File Size: %0.2f' % avgSizeHR)
	print('Traversal Time: %0.2f ms' % traversalTimeHR)

if __name__ == '__main__':
	main()