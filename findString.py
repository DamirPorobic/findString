#!/usr/bin/env python

# Written by Damir Porobic <damir_porobic@live.com>

import sys, getopt, os

# Function that prints the help menu
def printHelp():
	print "Usage: findString.py -s <Search String> [-d] <Search Directory> [-c] <String>\n"
	print "\t-s, --searchString\t The string to search for. This is required."
	print "\t-d, --searchDirectory\t The location of the files that are searched, by default, current directory."
	print "\t-c, --contains\t\t Only files that contain the provided string will be searched.\n"

searchDirectory = ''
searchString = ''
containsString = ''

# Try to parse command line argmunets 
try:
	opts, args = getopt.getopt(sys.argv[1:], "hs:d:c:", ["help", "searchString=", "searchDirectory=", "contains="])
except getopt.GetoptError:
	printHelp()
	sys.exit(2)

for opt, arg in opts:
	if opt in ("-h", "--help"):
		printHelp()
		sys.exit()
	elif opt in ("-s","--searchString"):
    	searchString = arg
	elif opt in ("-d","--searchDirectory"):
		searchDirectory = arg
	elif opt in ("-c", "--contains"):
		containsString = arg

# Check if we have a search string, if not, exit, unable to proceed
if not searchString:
	print "Unable to proceed without search string!"
	printHelp()
	sys.exit(2)

# Check if we have a search directory, if no, use current directory
if not searchDirectory:
	searchDirectory = os.getcwd()

# Get all files from directory
f = []
for (dirpath, dirnames, filenames) in os.walk(searchDirectory):
	f.extend(filenames)
	break

# Open one file after the other
for file in filenames:
	if containsString.upper() not in file.upper():
		continue
  
	with open(searchDirectory + '/' + file) as f:
		content = f.readlines()
	
	segment = []
	haveMatch = False
	headerPrinted = False
	
	# Loop through every line
	for line in content:
		# Check if we have a new segment
		if not line.startswith(' '):
			# We are starting with a new segment, check if we had
			# a match in last segment, if yes, print it out		
			if haveMatch:
				# Print file header only for files where we have a match 
				if not headerPrinted:
					print '=============== ' + file + ' ===============\n'
					headerPrinted = True
				sys.stdout.write("".join(segment))
				print "\n"
			# Segment was printed, clear buffer, prepare for next
			haveMatch = False
			segment = []
		
		# Check if we have a string match in current line
		if searchString in line:
			haveMatch = True
		# Add line to current segment
		segment.append(line)