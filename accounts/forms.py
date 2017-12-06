from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import Company



class profileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','email']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ("email", "password1", "password2")

    def save(self, company, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"]

        user.email = email
        user.company = company

        if commit:
            user.save()

        return user

class UserLoginForm(AuthenticationForm):
    """
    Authentication form that accepts an email/username and a password.
    """
    email = forms.CharField(label = "Email", max_length="255")

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['is_active']







