from django.db import models
from accounts.models import Company
from django.conf import settings


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
        related_name="followed_project"
        )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("company", "name"))


class Task(models.Model):
    """
    Model for tasks in a project.
    """
    company = models.ForeignKey(Company)
    project = models.ForeignKey(Project, related_name="tasks")
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    assigned = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="tasks"
        )
    complete = models.BooleanField(default=False)
    related_experiment = models.ForeignKey('app.Experiment', null=True)
    due_date = models.DateField(null=True)
