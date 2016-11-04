# 
# Developed by Praveen Kumar. 
# 

def main():
	from pyteomics import mzml
	import subprocess
	import os
	import sys
	import re
	import pandas as pd
	from operator import itemgetter
	from itertools import groupby
	if len(sys.argv) >= 5:
		# Start of Reading Scans from PSM file
		# Creating dictionary of PSM file: key = filename key = list of scan numbers
		ScanFile = sys.argv[2]
		spectrumTitleList = list(pd.read_csv(ScanFile, "\t")['Spectrum Title'])
		scanFileNumber = [[".".join(each.split(".")[:-3]), int(each.split(".")[-2:-1][0])] for each in spectrumTitleList]
		scanDict = {}
		for each in scanFileNumber:
			if scanDict.has_key(each[0]):
				scanDict[each[0]].append(int(each[1]))
			else:
				scanDict[each[0]] = [int(each[1])]
		# End of Reading Scans from PSM file
		
		inputFile = sys.argv[1]
		outPath = "/".join(sys.argv[3].split("/")[:-1])
		outFile = sys.argv[3].split("/")[-1]
		allScanList = []
		
		# Read all scan numbers using indexedmzML/indexList/index/offset tags
		for k in mzml.read(inputFile).iterfind('indexedmzML/indexList/index/offset'):
			if re.search("scan=(\d+)", k['idRef']):
				a = re.search("scan=(\d+)", k['idRef'])
				allScanList.append(int(a.group(1)))
		# End of Reading mzML file
		
		scan2remove = scanDict[sys.argv[4]]
		scan2retain = list(set(allScanList) - set(scan2remove))
		scan2retain.sort()
		# scan2retain contains scans that is to be retained
		
		
		print "Total number of Scan Numbers: " + len(list(set(allScanList))) + "\n"
		print "Number of Scans retained: " + len(list(set(scans2remove))) + "\n"
		print "Number of Scans retained: " + len(scan2retain) + "\n"
		
		
		# Identifying groups of continuous numbers in the scan2retain and creating scanString
		scanString = ""
		for a, b in groupby(enumerate(scan2retain), lambda(i,x):i-x):
			x = map(itemgetter(1), b)
			scanString = scanString + "["+str(x[0])+","+str(x[-1])+"] "
		# end identifying
		
		os.system("ln -s "+inputFile+" "+sys.argv[4]+".mzml")
		
		# Prepare command for msconvert
		msconvert_command = "msconvert " +sys.argv[4]+".mzml"+ " --filter " + "\"scanNumber " + scanString + " \" " + " --outfile " + "filtered_"+sys.argv[4]+".mzml" + " --mzML"
		# print msconvert_command
		
		# Run msconvert
		os.system(msconvert_command)
		
		# Renaming command
		allFiles = os.listdir(outPath)
		fileCreated = ''
		for each in allFiles:
			if re.search(outFile+"\..+", each):
				fileCreated = each
		# Copy output to 
		os.system("cp filtered_"+sys.argv[4]+".mzml " + outPath + "/" + outFile)
		
	else:
		print "Please contact the admin. Number of inputs are not sufficient to run the program.\n"

if __name__ == "__main__":
	main()
	
	
	
	