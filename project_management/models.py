from django.db import models
from accounts.models import Company
from django.conf import settings
from inventory.models import Item


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


class CompletedTaskManager(models.Manager):
    """
    manager for getting completed tasks.
    """
    def get_queryset(self):
        return super().get_queryset().filter(complete=True)


class IncompleteTaskManager(models.Manager):
    """
    manager for getting incomplete tasks.
    """
    def get_queryset(self):
        return super().get_queryset().filter(complete=False)


class Task(models.Model):
    """
    Model for tasks in a project.
    """
    company = models.ForeignKey(Company)
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    assigned = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
        null=True
        )
    complete = models.BooleanField(default=False)
    related_experiment = models.ForeignKey('app.Experiment', null=True)
    due_date = models.DateField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    completed = CompletedTaskManager()
    incomplete = IncompleteTaskManager()

    class Meta:
        ordering = ['timestamp']
        unique_together = (('project', 'name'))
