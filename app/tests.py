from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
import json
from .models import Experiment

# Create your tests here.


class initialTest(TestCase):

    def setUp(self):
        self.experiment = Experiment.objects.create(
            reactor_diameter = 12,
            reactor_length = 6,
            num_chambers = 12,
            removal_target = "E.Coli",
            reactor_age = 1000)
        

    def test_experiment_creation(self):
        self.assertEqual(self.experiment, Experiment.objects.get(id=self.experiment.id))
    
# View tests

class formTest(TestCase):
    def setUp(self):
        self.client = Client()
        reverse("upload_form")
        
    # no experiment data entered
    def test_empty_form(self):
        data = {"metadata-Chambers" : "1", "metadata-Diameter": "1" , "metadata-Length": "5", "metadata-Target": "target", "metadata-Age (mL)": '', "exp_data-json": json.dumps({'':'','':''})}
        response = self.client.post(reverse("upload_form"), data)
        
        self.assertRedirects(response, reverse("upload_error"))
        
    def test_valid_form(self):
        data = {"metadata-Chambers" : "1", "metadata-Diameter": "1" , "metadata-Length": "5", "metadata-Target": "target", "metadata-Age (mL)": '', "exp_data-json": json.dumps({'some field':'value','field 2':'value'})}
        
        exp_id = Experiment.objects.last()
        
        response = self.client.post(reverse("upload_form"), data)
      
class csvTest(TestCase):
    def test_blank_csv(self):
        pass
        
    def test_wrong_format(self):
        pass
        
    def test_missing_metadata(self):
        pass
        
    def test_valid_csv(self):
        pass
        

class templateTest(TestCase):
    def test_save_empty_template(self):
        pass
        
    def test_save_existing_name(self):
        pass
        
    def test_save_existing_templates(self):
        pass
        
    def test_save_template(self):
        pass
        
    def test_get_existing_template(self):
        pass
        
    def test_get_non_existing_template(self):
        pass
    
class autocompleteTest(TestCase):
    def test_field_match(self):
        pass
        
    def test_no_match(self):
        pass
        
