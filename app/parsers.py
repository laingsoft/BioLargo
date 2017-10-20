from abc import ABC, abstractclassmethod
import csv 
from ast import literal_eval
from app.models import Experiment, ExperimentData, Fields
from magic import from_buffer
import copy
import json
            
# if file type is not known, create Parser object.
#~ parser = Parser(fp, metadata_fields, user)
#~ parser = parser.get_parser()
#~ then get data from parser or whatever. Does NOT save to db until 
#~ parser.create_objects(group, tags) is called.

# Abstract base parser class. 
#~ Implements all non-filetype specific operations like creating objects
#~ and getters and setter
class BaseParser(ABC):
    def __init__(self, fp, metadata_fields, user):
        self.fp = fp
        self.metadata_fields = metadata_fields
        self.metadata = dict() 
        self.data = [] # a list of dictionaries
        self.comments = [] # a list of strings
        self.user = user 
        self.experiment = None
        
    @abstractclassmethod
    def parse(self):
        pass
        
    def reformat_data(self):
        # move fields around if needed.  
        move = {} 
        for field in self.metadata.keys():
            if field not in metadata:
                move[field] = metadata[field]
                del(metadata[field])

        # pull out comments + add extra fields to each row
        for row in self.data:
            if row[self.comment_field]:
                self.comments.append(row[self.comment_field])
            row.update(move)
        
    
    def create_objects(self, group, tags):
        # Create the fields if they don't already exist
        for item in self.parsed[data][0].keys():
            field = Field.objects.get_or_create(name=item.lower())
            
        # Create Experiment object
        self.experiment = Experiment(
            metadata = self.metadata, 
            user = user) # TODO: add other parameters (forgot what else goes here)
        
        # add tags
        self.experiment.tags.add(*tags)
         
        self.experiment.save()
        
        # create comments
        for comment in self.comments:
            c = Comment(experiment = self.experiment, User = self.user, content = comment)
            c.save()
            
        # Create ExperimentData objects
        for line in self.data:
            data = ExperimentData(experiment = self.experiment, experimentData = line)
            data.save()
            
    # returns copies of all data in the objects. So objects don't get
    #~ accidentally modified, a copy of everything is returned
    def get_parsed(self):
        return {'metadata': copy.deepcopy(self.metadata), 
        'data':copy.deepcopy(self.data), 
        'comments':copy.deepcopy(self.comments)}
        
    def set_metadata(self, metadata):
        self.metadata = metadata
        
    def set_data(self, data):
        self.data = data
    
    def set_comments(self, comments):
        self.comments = comments
        
    def get_experiment(self):
        return self.experiment.id
'''
csv parser
This parser will work with any plaintext file with a delimiter. 
The parser will assume the metadata is a separate line at the 
beginning of the file
'''
class CsvParser(BaseParser):
    def __init__(self, fp, metadata_fields, user, comment_field = "comments"):
        super().__init__(fp, user, metadata_fields)
        try:
            self.delimiter = find_delmiter()
        except: 
            raise ValueError 
            
        self.comment_field = comment_field
        
        parse()
                
    def parse(self):
        reader = csv.DictReader(csv_file)
        
        self.metadata = next(reader)
        
        try:
            del metadata[''] # remove empty key from trailing comma
        except KeyError:
            # do nothing if there is no trailing comma
            pass

        reader = csv.DictReader(csv_file)
        
        for line in reader:
            self.data.append(line)
            
        reformat_data()
        
        
'''
JSON Parser
========================================================================
#JSON structure expected:
        { 
        "metadata": {
                "field1" : value,
                "field2": value,
                ...
            },
        "data":[
            {
                "field1": value,
                "field2": value,
                ...
                },
            {
                "field1": value,
                "field2": value,
                },
            ...
            ]
        "comments":[
            {
                "person": person,
                "content": content
                },
            {
                "person": person,
                "content": content
                }
            ...
            ]
        }
========================================================================
This parser is used by the upload form (sends JSON to server)
Does allow user to upload JSON as well, but who would do that...
'''
class JsonParser(BaseParser):
    def __init__(self, **kwargs):
        super().__init__(fp, metadata_fields, user)
        
    def parse(self):
        data = self.fp.read()
        data = json.loads(data) # Will throw ValueError if not valid JSON
        
        
        # will throw KeyError if not expected format
        self.metadata = data['metadata']
        self.data = data['data']
        self.comments = data['comments']
        
# dictionary of available parsers. 
# the key is the first part of the output of the file command.
parsers = {
    'CSV' : CsvParser,
    'JSON' : JsonParser,
}

# a wraper class to create the parser based on file type. Will find the 
# file type 
class Parser():
    def __init__(self, file_type = None, **kwargs):
        if file_type:
            self.file_type = file_type
        else:
            self.file_type = find_file_type() 

        # remember to catch the key error if file type not supported in view
        self.parser = parsers[self.file_type](**kwargs)
        
    def get_parser(self):
        return self.parser
        
    # determines file type using MIME type, magic number and file extension 
    def find_file_type(self):
        pass
        
