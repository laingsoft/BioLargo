from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager
from django.utils import timezone


# Create your models here.


    


class Plan(models.Model):
    """
    Available plans. if is_active is true, then it is shown on the pricing page
    and can be used to register a new company.
    """
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Company(models.Model):
    """
    Stores a single company. Is used to determine owner of all data
    """
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    good_standing = models.BooleanField(default = True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
    
class Payment(models.Model):
    date_payed = models.DateTimeField(_('date payed'), default=timezone.now)
    date_next_due = models.DateTimeField(_('date next due'), default=timezone.now)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    balance = models.FloatField()
    
    

class User(AbstractBaseUser, PermissionsMixin):
    """
    Model used to store users. A user must belong to a company.

    Taken from https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractbaseuser
    2017/12/04
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # user gets deleted if company is deleted.
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    show_tutorial = models.BooleanField(default=True)

    # For accessing management panel
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    # for accessing admin panel
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        unique_together = (('company', 'email'))

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name
        '''

        name = self.first_name + ' ' + self.last_name or self.email
        return name

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name


class Invite(models.Model):
    """
    Stores invite information.
    The hash is company + date + email.

    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=64)  # SHA256 hash

    def validate(self):
        """
        checks if the link is still active. The link expires after 24 hours.
        Returns True if link is valid, else False.
        """
        now = datetime.datetime.now()
        diff = now - self.date
        if diff.days > 0:
            return False

        return True
