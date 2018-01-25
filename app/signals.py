from .models import Notification, Comment, Experiment
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Comment)
def comment_save_reciever(sender, instance, **kwargs):
    """
    reciever that notifies all users watching an experiment or a project on
    a new comment
    """

    recipients = instance.experiment.followers.all()
    if recipients.exists():
        notification = Notification.objects.create(
            subject=instance.user,
            predicate="COM",
            object_type="EXP",
            object_pk=instance.experiment.pk,
            content=instance.content[:255]
            )

        notification.recipients.add(*list(recipients))


@receiver(post_save, sender=Experiment)
def experiment_update_reciever(sender, instance, created, **kwargs):
    """
    reciever that notifies users that a watched experiment has been updated
    """
    if not created:
        recipients = instance.followers.all()

        if recipients.exists():
            notification = Notification.objects.create(
                subject=instance.user,
                predicate="EXP",
                object_type="UPD",
                object_pk=instance.pk,
                )
            notification.recipients.add(*list(recipients))


@receiver(post_save, sender=Experiment)
def experiment_upload_reciever(sender, instance, created, **kwargs):
    """
    reciever that creates notification for an experiment uploaded to a watched
    project
    """

    if created:
        recipients = instance.project.followers.all()

        if recipients.exists():
            notification = Notification.objects.create(
                subject=instance.user,
                predicate="PRJ",
                object_type="PRJ",
                object_pk=instance.project.pk,
                content="<a href='/app/experiment/{0}'>{1}</a>".format(
                    instance.pk,
                    instance.friendly_name
                )
            )
            notification.recipients.add(*list(recipients))
