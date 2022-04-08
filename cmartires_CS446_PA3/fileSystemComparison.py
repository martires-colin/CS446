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
	fileInfo = {}
	dirInfo = {}

	dirs = next(os.walk(filePath))[1]
	for dirName in dirs:
		fileSize = os.path.getsize(filePath + '/' + dirName)
		dirInfo[dirName] = fileSize
	
		files = next(os.walk(filePath + '/' + dirName))[2]
		for fileName in files:
			fileSize = os.path.getsize(filePath + '/' + dirName + '/' + fileName)
			fileInfo[fileName] = fileSize

	files = next(os.walk(filePath))[2]
	for fileName in files:
		fileSize = os.path.getsize(filePath + '/' + fileName)
		fileInfo[fileName] = fileSize

	return fileInfo, dirInfo

def writeDataFile(data, fileName, destination):
	origin = os.getcwd()
	os.chdir(destination)
	f = open(fileName, "a")
	for key, value in data.items():
		f.write('File Name: %s\nFile Size: %s bytes\n\n' % (key,value))
	f.close()
	os.chdir(origin)

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
	SRFileData, SRDirData = traverseDirectory('/home/cmartires/singleRoot')			#traverse singleRoot
	timeEndSR = time.time()												#end timer for singleRoot traversal
	
	timeStartHR = time.time()											#start timer for hierarchicalRoot traversal
	HRFileData, HRDirData = traverseDirectory('/home/cmartires/hierarchicalRoot')		#traverse hierarchicalRoot
	timeEndHR = time.time()												#end timer for hierarchical traversal

	writeDataFile(SRFileData, 'singleLevelFiles.txt', '/home/cmartires/singleRoot')		#write data to file					#write files with directory info
	writeDataFile(HRFileData, 'hierarchicalFiles.txt', '/home/cmartires/hierarchicalRoot')
	writeDataFile(HRDirData, 'hierarchicalFiles.txt', '/home/cmartires/hierarchicalRoot')

	avgFileSizeSR = calculateAvgSize(SRFileData)								#calculate average file size
	avgFileSizeHR = calculateAvgSize(HRFileData)
	avgDirSizeHR = calculateAvgSize(HRDirData)

	traversalTimeSR = (timeEndSR - timeStartSR) * 1000					#calculate traversal time
	traversalTimeHR = (timeEndHR - timeStartHR) * 1000

	print('singleRoot Statistics:')
	print('Number of Files:', len(SRFileData))
	print('Average File Size: %0.2f bytes' % avgFileSizeSR)
	print('Traversal Time: %0.2f ms' % traversalTimeSR)
	
	print('\nhierarchicalRoot Statistics:')
	print('Number of Files:', len(HRFileData))
	print('Average File Size: %0.2f bytes' % avgFileSizeHR)
	print('Number of Directories:', len(HRDirData))
	print('Average Directory Size: %0.2f bytes' % avgDirSizeHR)
	print('Traversal Time: %0.2f ms' % traversalTimeHR)

if __name__ == '__main__':
	main()