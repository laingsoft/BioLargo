from django.test import TestCase
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
    
