from django import forms
from .models import Scientist
from django.contrib.auth.models import User


class profileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

