from abc import ABC, abstractclassmethod
import csv
from ast import literal_eval
from app.models import ExperimentData, Fields, Comment
from magic import from_buffer # file type identification isn't implemented.
import json
from datetime import datetime
from django.db import transaction, IntegrityError
from django.http import HttpResponseServerError

# if file type is not known, create Parser object.
# parser = Parser(fp, metadata_fields, user)
# parser = parser.get_parser()
# then get data from parser or whatever. Does NOT save to db until
# parser.create_objects(project, tags) is called.


class BaseParser(ABC):
    """
    Abstract base parser class.
    Implements all non-filetype specific operations like creating objects
    and getters and setter.

    Takes a buffer as an argument.
    """

    def __init__(self, *args, **kwargs):
        try:
            self.buffer = kwargs.get('buffer')
        except KeyError:
            raise ValueError("buffer argument required.")

        self.metadata = dict()
        self.data = []  # a list of dictionaries
        self.comments = []  # a list of strings
        self.errors = {}
        self.comment_field = kwargs.get('comment_field', "Comments")

    @abstractclassmethod
    def parse(self):
        """
        must be implemented by subclasses.
        """
        pass

    def reformat_data(self):
        """
        Moves data to whatever type it is. Currently only moves comments from
        experiment data.
        """
        for row in self.data:
            try:
                self.comments.append(row.pop(self.comment_field).strip())
            except KeyError:
                pass
                # do nothing if no comment field or comment field name not correct.

    def create_objects(self, experiment):
        """
        Creates ExperimentData and Comment objects. Takes an experiment object
        as an argument.
        """

        company = experiment.company

        try:
            with transaction.atomic():
                # Create the fields if they don't already exist
                for item in {**self.data[0], **self.metadata}.keys():
                    Fields.objects.get_or_create(company=company, name=item.lower())

                experiment.metadata = self.metadata
                experiment.save()

                # create comments
                for comment in self.comments:
                    if comment.strip():
                        Comment.objects.create(experiment=experiment, user=experiment.user, content=comment, company=company)

                # Create ExperimentData objects
                for line in self.data:
                    if any(line.values()):
                        ExperimentData.objects.create(experiment=experiment, experimentData=line, company=company)
        except IntegrityError:
            raise HttpResponseServerError

    def get_parsed(self):
        """
        Returns parsed objects
        """
        return self.metadata, self.data, self.comments


class CsvParser(BaseParser):
    """
    This parser will work with any plaintext file with a delimiter.
    The parser will assume the metadata is in two separate lines at the
    beginning of the file (header in one row, values in the next)
    Delimiter will default to a comma if none is given.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.delimiter = kwargs.get('delimiter', ',')
        self.parse()

    def parse(self):
        reader = csv.DictReader(self.buffer)

        self.metadata = next(reader)

        try:
            del self.metadata['']  # remove empty key from trailing comma
        except KeyError:
            # do nothing if there is no trailing comma
            pass

        reader = csv.DictReader(self.buffer)

        for line in reader:
            self.data.append(line)

        self.reformat_data()


class JsonParser(BaseParser):
    """
    Parses JSON data.

    Expected keys:
     - metadata
     - data
     - comments

    This parser is used by the upload form (sends JSON to server)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parse()

    def parse(self):
        data = self.buffer.read()
        data = json.loads(data)  # Will throw ValueError if not valid JSON

        # will throw KeyError if not expected format
        self.metadata = data['metadata']
        self.data = data['data']
        self.comments = data.get('comments', [])

        self.reformat_data()


class Parser():

    """
    a wraper class to create the parser based on file type. Will find the
    file type
    """

    PARSERS = {
        'CSV': CsvParser,
        'JSON': JsonParser,
    }

    def __init__(self, file_type=None, **kwargs):
        if file_type:
            self.file_type = file_type
        else:
            self.file_type = self.find_file_type()

        # remember to catch the key error if file type not supported in view
        self.parser = self.PARSERS[self.file_type](**kwargs)

    def get_parser(self):
        return self.parser

    # determines file type using MIME type, magic number and file extension
    def find_file_type(self):
        return "CSV"  # TODO: implement this function.
