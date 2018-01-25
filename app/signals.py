from .models import Notification, Comment
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
