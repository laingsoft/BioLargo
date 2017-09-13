import csv
from ast import literal_eval
#from models import Experiment
import json

#Constants

METAFIELDS = ["Person", 
"Reactor Diameter [inch]", 
"Reactor Length [inch]", 
"#Chambers", 
"Date (d/m/y)", 
"Removal Target", 
"Age of reactor [L]"]

# Reads the CSV data and adds data read to database
# inputs: a filename
# returns: Nothing

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
	
	eData = []
	
	for line in reader:
		for item in line:
			try:
				line[item] = literal_eval(line[item])
			except:
				pass
				
		eData.append(line)
		
	data.close()
	
	metadata, edata = reformatData(metadata, eData)

	exp = Experiment(experimentMeta = json.dumps(metadata), 
	experimentData = json.dumps(eData))
	exp.save()
	
	
# moves extra metadata fields to the experiment data
# inputs: 
# 1. metadata dictionary
# 2. list of dictionaries of experiment data
# returns: same as inputs. 

def reformatData(metadata, eData):
	
	move = dict()
	
	metaKeys = metadata.keys()
	# check for any extra metadata fields and delete.
	for field in metaKeys:
		if field not in METAFIELDS:
			move[field] = metadata[field]
			del metadata[field]
			

	 # add the extra metadata fields to the experiment data
	for exp in eData:
		exp.update(move)
		
	return metadata, eData
	
	
	
