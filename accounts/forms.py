from django import forms
from .models import Scientist
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm



class profileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username','first_name','last_name','email']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ("email", "password1", "password2")

    def save(self, company, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"]

        user.email = email
        user.username = email[:email.find('@')]
        user.company = company

        if commit:
            user.save()

        return user