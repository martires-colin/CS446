#Program Name: fileSystemComparison.py
#Author: Colin Martires
#Purpose: Programming Assignment 3
#This program will compare and contrast single-level and heirarchical file
#directories. The program will determine the size difference as well as the
#traversal time between the two types of directories.

# COMPARE THE THINGIES

# To Do
#

import os

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
		# print(dirName, '-', fileSize)
		dirInfo[dirName] = fileSize
	
		files = next(os.walk(filePath + '/' + dirName))[2]
		for fileName in files:
			fileSize = os.path.getsize(filePath + '/' + dirName + '/' + fileName)
			# print(fileName, '-', fileSize)
			dirInfo[fileName] = fileSize

	files = next(os.walk(filePath))[2]
	for fileName in files:
		fileSize = os.path.getsize(filePath + '/' + fileName)
		# print(fileName, '-', fileSize)
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
	createDirectories('/home/cmartires/hierarchicalRoot', 10)			#generate directories?files within hierarchicalRoot

	SRdata = traverseDirectory('/home/cmartires/singleRoot')			#traverse directories
	HRdata = traverseDirectory('/home/cmartires/hierarchicalRoot')

	numSRfiles = writeDataFile(SRdata, 'singleLevelFiles.txt', '/home/cmartires/singleRoot')						#write files with directory info
	numHRfiles = writeDataFile(HRdata, 'hierarchicalFiles.txt', '/home/cmartires/hierarchicalRoot')

	avgSizeSR = calculateAvgSize(SRdata)
	avgSizeHR = calculateAvgSize(HRdata)

	print('Number of files in singleRoot:', numSRfiles)
	print('Average File Size in singleRoot: %0.2f' % avgSizeSR)
	print('Number of files in hierarchicalRoot:', numHRfiles)
	print('Average File Size in hierarchicalRoot: %0.2f' % avgSizeHR)


if __name__ == '__main__':
	main()