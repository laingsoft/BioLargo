from .models import Notification


def notify_users(sender, instance, **kwargs):
    """
    reciever that notifies all users watching an experiment or a project on
    an update.
    """
    users = instance.followers.all()
    if users.exists():
        notification = Notification.create()
        notification.recipients.add(*list(users))
