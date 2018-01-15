from django import forms
from app.models import Fields, Template, Experiment
from .models import GroupExtra
from django.contrib.auth import get_user_model
from .models import Settings
from django.contrib.auth.models import Group


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        exclude = ('company',)


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


class GroupForm(forms.ModelForm):
    description = forms.CharField()

    class Meta:
        model = Group
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['description'].initial = self.instance.extra.description

    def save(self, **kwargs):
        """
        overridden save function for saving the extra description field.
        company is used in place of commit.
        requires company argument for saving extra
        """

        group = super().save()

        if self.instance:
            extra = group.extra
            extra.description = self.cleaned_data['description']

        else:
            extra = GroupExtra(description=self.cleaned_data['description'], group=group, company=kwargs.get('company'))

        extra.save()

        return group
