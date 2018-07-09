from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import Company
from django.contrib.auth import authenticate


class profileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        widgets = {"first_name":  forms.TextInput(attrs={'class': 'form-control'}), "last_name": forms.TextInput(attrs={'class': 'form-control'}), "email": forms.TextInput(attrs={'class': 'form-control'})}

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"]

        user.email = email

        if commit:
            user.save()

        return user


class UserLoginForm(AuthenticationForm):
    """
    Authentication form that accepts an email/username and a password.
    """
    email = forms.CharField(label="Email", max_length="255")

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
    name = forms.CharField(label="Company Name")

    class Meta:
        model = Company
        exclude = ['is_active', 'good_standing']
