from django.db import models
from accounts.models import Company
from django.conf import settings
from inventory.models import Item
from django.db.models import Q


class Project(models.Model):
    """
    Stores projects with a start and end date, and a description of the
    project.
    """
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="followed_project", blank = True
        )


    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("company", "name"))


class IncompleteTaskManager(models.Manager):
    """
    manager for getting incomplete tasks.
    """
    def get_queryset(self):
        return super().get_queryset().filter(Q(status='I') | Q(status='N') )


class Task(models.Model):
    """
    Model for tasks in a project.
    """

    STATUS = (
        ('N', 'Not started'),
        ('I', 'In progress'),
        ('C', 'Complete')
        )

    company = models.ForeignKey(Company)
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    assigned = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
        null=True
        )
    status = models.CharField(max_length=1, choices=STATUS, default='N')
    related_experiment = models.ForeignKey('app.Experiment', null=True)
    due_date = models.DateField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    sop = models.ForeignKey('SOP.SOP', null=True, blank=True)

    objects = models.Manager()
    incomplete = IncompleteTaskManager()


    class Meta:
        ordering = ['timestamp']
        unique_together = (('project', 'name'))
