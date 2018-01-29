from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from accounts.models import Company
from project_management.models import Project

# Create your models here.


class Tag(models.Model):
    """
    Stores tags for experiments. Stores tag name only.
    """
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("company", "name"))


class Experiment(models.Model):
    """
    Store experiments. Does not store the data for each experiment.
    """
    company = models.ForeignKey(Company)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    edit_timestamp = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    metadata = JSONField(default='')
    friendly_name = models.CharField(max_length=255)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followed_experiments")


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
    empty = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name_plural = "fields"
        unique_together = (("company", "name"))

    def __str__(self):
        return self.name


class Template(models.Model):
    """
    Stores templates. It is a collection of predefined fields.
    """
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)
    fields = models.ManyToManyField(Fields)
    metadata = models.ManyToManyField(Fields, related_name="metadata_fields")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("company", "name"))


class Comment(models.Model):
    """
    Stores comments on experiments.
    """
    company = models.ForeignKey(Company)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class UnreadNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(read=False)


class Notification(models.Model):
    """
    Model for notifications.
    Notifications are in format
    <Subject> <Predicate> <Object>
    Subject: user who performed action
    Predicate: what the action was
    Object: the watched object

    content is extra information, such as a link to the experiment uploaded or
    the comment contents.

    object_name is either Experiment.friendly_name or Project.name
    """
    PREDICATES = (
        ("COM", "commented on"),
        ("PRJ", "uploaded a new experiment to"),
        ("UPD", "updated experiment")
    )

    OBJECT_TYPES = (
        ("EXP", "experiment"),
        ("PRJ", "project"),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications")
    subject = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="activity")
    predicate = models.CharField(max_length=3, choices=PREDICATES)
    object_type = models.CharField(max_length=3, choices=OBJECT_TYPES)
    object_pk = models.IntegerField()
    object_name = models.CharField(max_length=255, blank=True)
    content = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    objects = models.Manager()
    unread = UnreadNotificationManager()


