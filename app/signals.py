from .models import Notification, Comment, Experiment
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice
import pyfcm


@receiver(post_save, sender=Comment)
def comment_save_reciever(sender, instance, **kwargs):
    """
    reciever that notifies all users watching an experiment or a project on
    a new comment
    """
    
    recipients = instance.experiment.followers.all()
    if recipients.exists():
        notifications = []
        args = {
            "subject": instance.user,
            "predicate": "COM",
            "object_type": "EXP",
            "object_pk": instance.experiment.pk,
            "content": instance.content[:255],
            "object_name": instance.experiment.friendly_name,
        }
        for r in recipients:
            if(instance.user != r):
                notifications.append(Notification(**args, recipient=r))
                sendPushNotification(r, instance, 0)   
        
        Notification.objects.bulk_create(notifications)



@receiver(post_save, sender=Experiment)
def experiment_update_reciever(sender, instance, created, **kwargs):
    """
    reciever that notifies users that a watched experiment has been updated
    """
    if not created:
        recipients = instance.followers.all()

        if recipients.exists():
            notifications = []
            args = {
                "subject": instance.user,
                "predicate": "EXP",
                "object_type": "UPD",
                "object_pk": instance.pk,
                "object_name": instance.friendly_name,
            }

            for r in recipients:
                if(instance.user != r):
                    notifications.append(Notification(**args, recipient=r))
                    sendPushNotification(r, instance, 1)

            Notification.objects.bulk_create(notifications)



@receiver(post_save, sender=Experiment)
def experiment_upload_reciever(sender, instance, created, **kwargs):
    """
    reciever that creates notification for an experiment uploaded to a watched
    project
    """

    if created:
        recipients = instance.project.followers.all()

        if recipients.exists():
            notifications = []
            args = {
                "subject": instance.user,
                "predicate": "PRJ",
                "object_type": "PRJ",
                "object_pk": instance.project.pk,
                "object_name": instance.project.name,
                "content": "<a href='/app/experiment/{0}'>{1}</a>".format(
                    instance.pk,
                    instance.friendly_name
                )
            }

            for r in recipients:
                if(instance.user != r):
                    notifications.append(Notification(**args, recipient=r))
                    sendPushNotification(r, instance, 2)

            Notification.objects.bulk_create(notifications)


#This function will send a push notification to the user "r" according to the "type" passed in
#type 0 = new comment
#type 1 = experiment updated
#type 2 = new upload
def sendPushNotification(r, instance, type):
    device = FCMDevice.objects.filter(id = r.id)
    if type == 0:
        message_body = str(instance.user.first_name) + " " + \
                str(instance.user.last_name) + " commented on " + str(instance.experiment.friendly_name) + " " + str(instance.content[:255])
    elif type == 1:
        message_body = str(instance.user.first_name) + " " + \
                    str(instance.user.last_name) + " updated " + str(instance.experiment.friendly_name)
    elif type == 2:
        message_body = str(instance.user.first_name) + " " + \
            str(instance.user.last_name) + " uploaded to " + str(instance.project.name)
    device.send_message(data={"type": 2, "title" : "New Experiment", "body" : message_body})