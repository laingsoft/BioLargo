from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from accounts.models import Company

# Create your models here.


class Group(models.Model):
    """
    Depricated. Used to store experiment group. Has been replaced by Project.
    Will remove this class once refactor is fully done.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Stores tags for experiments. Stores tag name only.
    """
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Experiment(models.Model):
    """
    Store experiments. Does not store the data for each experiment.
    """
    company = models.ForeignKey(Company)
    user = settings.AUTH_USER_MODEL
    project = models.ForeignKey(Project)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    edit_timestamp = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    metadata = JSONField(default='')
    friendly_name = models.CharField(max_length=255, default=0)

    def __str__(self):
        return ("Experiment| Group: {0} | metadata: {1}").format(str(self.group), str(self.metadata))

    def __repr__(self):
        return ("Experiment| Group: {0} | metadata: {1}").format(str(self.group), str(self.metadata))


class ExperimentData(models.Model):
    """
    Stores data for each experiment in JSON. The data types are validated
    using the Field data_type
    """
    company = models.ForeignKey(Company)

    class Meta:
        verbose_name_plural = "experiment data"

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    experimentData = JSONField()
    # More Experiment Data Here


class Fields(models.Model):
    """
    Stores fields for adding experiments with a data type that is enforced
    on upload.
    """
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)

    # the data type choices
    DATA_TYPE_CHOICES = (
        ('INT', 'Integer'),
        ('FLOAT', 'Decimal'),
        ('DATE', 'Date'),
        ('STRING', 'Text'),
        )
    data_type = models.CharField(
            max_length=6,
            choices=DATA_TYPE_CHOICES,
            default='STRING'
        )

    class Meta:
        verbose_name_plural = "fields"

    def __str__(self):
        return self.name


class Template(models.Model):
    """
    Stores templates. It is a collection of predefined fields.
    """
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)
    fields = models.ManyToManyField(Fields)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """
    Stores comments on experiments.
    """
    company = models.ForeignKey(Company)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
