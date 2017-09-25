from django.test import TestCase
from .models import Customer
from django.contrib.auth.models import User
# Create your tests here.
class Accounts(TestCase):
    def setUp(self):
        self.loggedinuser = User.objects.create_user(
            username = "steven", email="sjohnson@steve.com", password="stevespass")
        Customer.objects.create(
            first_name = "Steve", last_name = "Johnson",
            phone = "2222222222", email="sjohnson@steve.com",
            organization = "Ualberta", plan="basic", userObject = self.loggedinuser)

    def test_Customer_exists(self):
        steve = Customer.objects.get(first_name="Steve")
        self.assertEqual(steve.last_name, "Johnson")
        self.assertEqual(steve.userObject, self.loggedinuser)

        
