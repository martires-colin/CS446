# Program Name: fileSystemComparison.py
# Author: Colin Martires
# Purpose: Programming Assignment 3
# This program will compare and contrast single-level and heirarchical file
# directories. The program will determine the size difference as well as the
# traversal time between the two types of directories.

# -------------singleLevelFiles.txt vs hierarchicalFiles.txt---------------------------
# Both text files contain 100 files with a size of 0 bytes. The difference is
# that in hierarchicalRoot, the files are sorted into 10 subdirectories each containing
# 10 of the 100 total files generated. This means that when printing the file data to
# hierarchicalFiles.txt, the 10 subdirectories will be included. singleLevelFiles.txt
# contains 100 files of size 0 bytes while hierarchicalFiles.txt contains 100 files of
# size 0 bytes and 10 files of size 4096 bytes. 

# -------How can we implement something similar to a hierarchical file system?---------
# Since we can't have subdirectories in single-level file system, a file path like
# /home/sarad/Downloads/test.txt would not exist. A way to approximate the file path
# is to translate the file path into a file name. The "/" is an illegal character in file
# naming conventions, so I would replace all the "/" with "-". What we end up with is 
# home-sarad-Downloads-test.txt, which would be an acceptable file in a single-level file
# directory. To mimic the organization of a hierarchical file system, we can use the 
# glob module. Using the glob function allows us to search for specific files with names
# that match a user-defined string. For example, executing glob.glob("home-sarad-Downloads-*.txt")
# would return all .txt files containing "home-sarad-Downloads-", which mimics the function 
# of changing into the Downloads directory. In summary, by stating the file path within
# the file name, we can organize files and filter through them using the glob function. 

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

def writeDataFile(data, fileName, destination, fileConfig):
	origin = os.getcwd()
	os.chdir(destination)
	f = open(fileName, fileConfig)
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

	# create directories
	os.makedirs('/home/cmartires/singleRoot', exist_ok=True)
	os.makedirs('/home/cmartires/hierarchicalRoot', exist_ok=True)

	# generate files (createDirectories generates files within directories)
	generateFiles('/home/cmartires/singleRoot', 100, 0)
	createDirectories('/home/cmartires/hierarchicalRoot', 10)

	# traverse directories, record traversal times
	timeStartSR = time.time()
	SRFileData, SRDirData = traverseDirectory('/home/cmartires/singleRoot')
	timeEndSR = time.time()
	
	timeStartHR = time.time()
	HRFileData, HRDirData = traverseDirectory('/home/cmartires/hierarchicalRoot')
	timeEndHR = time.time()

	# write files containing file info, store in singleRoot and hierarchicalRoot
	writeDataFile(SRFileData, 'singleLevelFiles.txt', '/home/cmartires/singleRoot', 'w')
	writeDataFile(HRFileData, 'hierarchicalFiles.txt', '/home/cmartires/hierarchicalRoot', 'w')
	writeDataFile(HRDirData, 'hierarchicalFiles.txt', '/home/cmartires/hierarchicalRoot', 'a')

	# calculate average file size
	avgFileSizeSR = calculateAvgSize(SRFileData)
	avgFileSizeHR = calculateAvgSize(HRFileData)
	avgDirSizeHR = calculateAvgSize(HRDirData)

	# calculate traversal time in milliseconds
	traversalTimeSR = (timeEndSR - timeStartSR) * 1000
	traversalTimeHR = (timeEndHR - timeStartHR) * 1000

	# display statistics to terminal
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