import csv
from ast import literal_eval
from .models import *
import json
import datetime

#Constants

FIELDS = ["Person", 
"Reactor Diameter [inch]", 
"Reactor Length [inch]", 
"#Chambers", 
"Date (d/m/y)", 
"Removal Target", 
"Age of reactor [L]"]

# Reads the CSV data and adds data read to database
# inputs: a filename
# returns: experiment id

def read_csv(csv_file, g):
    reader = csv.DictReader(csv_file)
	
    metadata = next(reader)
	
    try:
        del metadata[''] # remove empty key from trailing comma
    except KeyError:
        pass
		
    reader = csv.DictReader(csv_file)
	
    eData = []
	
    for line in reader:
        eData.append(line)
		
    csv_file.close()
	
    reformat_data(metadata, eData)
    
    
    # add fields to database if it doesn't exist.
    f = eData[0].keys()
    for field in f:
        Fields.objects.get_or_create(name=field)[0].save()
    
    exp = Experiment(
    #person = metadata[FIELDS[0]],
    reactor_diameter = metadata[FIELDS[1]],
    reactor_length = metadata[FIELDS[2]],
    num_chambers = metadata[FIELDS[3]],
    #date = date_parser(metadata[FIELDS[4]]),
    removal_target = metadata[FIELDS[5]],
    reactor_age = metadata[FIELDS[6]] if is_float(metadata[FIELDS[6]]) else 0,
    group = g)
	
    exp.save()
	
    for line in eData:
        expData = ExperimentData(experiment = exp, experimentData = json.dumps(line))
        expData.save()
        
    return exp
        
	

# moves extra metadata fields to the experiment data
# inputs: 
# 1. metadata dictionary
# 2. list of dictionaries of experiment data
# returns: nothing. Items are modified directly.

def reformat_data(metadata, eData):
	
    move = dict()
	
    metaKeys = metadata.keys()
	# check for any extra metadata fields and delete.
    for field in metaKeys:
        if field not in FIELDS:
            move[field] = metadata[field]
            del metadata[field]
            
    # add the extra metadata fields to the experiment data
    for item in eData:
        item.update(move)


	
# parses date string. Exists because the delimiter isn't the same
# for all files.
# input: date as a string
# returns: datetime.date object

def date_parser(dateString):
	# find the delimiter
	delimiter = "" 
	for char in dateString:
		if not char.isdigit():
			delimiter = char
			break
			
	dateFormat = "%d{0}%m{0}%Y".format(delimiter)
	
	return datetime.datetime.strptime(dateString, dateFormat).date()


def is_float(val):
    try:
        float(val)
    except ValueError:
        return False
        
    return True
