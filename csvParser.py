import csv
from ast import literal_eval

# Reads the CSV data
# inputs: a filename
# returns: 
# 1. a dictionary of metadata
# 2. a list of dictionaries of run data.
# Will update or add function to output the correct data structure later
def readCSV(fileName):
		
	data = open(fileName, 'r')
	reader = csv.DictReader(data)
	
	metadata = next(reader)
	del metadata[''] # remove empty key from trailing comma
	
	# data type conversion
	for item in metadata:
		try:
			metadata[item] = literal_eval(metadata[item])
		except:
			pass
	reader = csv.DictReader(data)
	
	runs = []
	
	for line in reader:
		for item in line:
			try:
				line[item] = literal_eval(line[item])
			except:
				pass
				
		runs.append(line)
		
	data.close()
		
	return metadata, runs

	
	
