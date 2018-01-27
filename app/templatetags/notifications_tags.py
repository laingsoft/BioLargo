from app.models import Notification
from django import template

register = template.Library()


@register.simple_tag
def unread_notifications(user):
    return Notification.unread.filter(recipient=user)
