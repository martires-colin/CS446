#Program Name: cmartires_examine_system.py
#Author: Colin Martires
#Purpose: Programming Assignment 1

import subprocess

f = open("cmartires_systemDetails.txt", "w")
f.close()

def rwData(location, description):
	fin = open(location, "r")
	procData = fin.readlines()
	fin.close()

	f = open("cmartires_systemDetails.txt", "a")
	f.write(description + "\n")
	f.writelines(procData)
	f.write("\n")
	f.close()

def getBootTime():
	f = open("cmartires_systemDetails.txt", "a")
	f.write("4. Time that the system was last booted" + "\n")
	f.close()
	cmd = ['uptime', '-s']
	output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
	f = open("cmartires_systemDetails.txt", "ab")
	f.write(output)
	f.close()
	f = open("cmartires_systemDetails.txt", "a")
	f.write("\n")
	f.close()


rwData("/proc/cpuinfo", "1. CPU type and model:")
rwData("/proc/version", "2. Kernel version details:")
rwData("/proc/uptime", "3. Amount of time since last boot:")
getBootTime()
rwData("/proc/diskstats", "5. Number of disk requests made:")
rwData("/proc/stat", "6. Number of processes created since last boot (see 'processes'):")


