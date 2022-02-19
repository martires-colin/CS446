# Colin Martires
# CS446 Programming Assignment 1
# 2/18/2022

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


rwData("/proc/cpuinfo", "1. CPU type and model:")
rwData("/proc/version", "2. Kernel version details:")
rwData("/proc/uptime", "3. Amount of time since last boot:")
rwData("/proc/stat", "4. Time that the system was last booted (see 'btime'):")
rwData("/proc/diskstats", "5. Number of disk requests made:")
rwData("/proc/stat", "6. Number of processes created since last boot (see 'processes'):")