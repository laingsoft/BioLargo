from django import forms
from app.models import Fields, Template, Experiment
from django.contrib.auth import get_user_model

class SettingsForm(forms.Form):
    dateformat = forms.CharField(label="Format to Use for Dates", max_length=10)
    ataglance = forms.CharField(label="At A Glance Data", max_length = 100)


class TemplateForm(forms.ModelForm):
    """
    Form used to add and edit templates in management panel.
    """
    class Meta:
        model = Template
        exclude = ('company',)


class FieldForm(forms.ModelForm):
    """
    Form used to add and edit fields in management panel.
    """

    class Meta:
        model = Fields
        exclude = ('company',)


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ("friendly_name", "project", "tags", "metadata")
        widgets = {
            "metadata": forms.HiddenInput()
        }


class UserChangeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        help_text="Change user password"
        )

    class Meta:
        model = get_user_model()
        exclude = ('company', 'is_active', 'last_login', 'date_joined', 'is_staff', 'is_superuser', 'password')

    def save(self, commit=True):
        """
        overriden to save user password if provided.
        """
        if self.data.get('password', None):
            user = super().save(commit=False)
            user.set_password(self.data['password'])
            user.save()

            return user

        else:
            return super().save()
