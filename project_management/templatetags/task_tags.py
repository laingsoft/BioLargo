from django import template
from project_management.models import Task

register = template.Library()


@register.simple_tag
def incomplete_tasks(user):
    return Task.incomplete.filter(assigned=user)


@register.simple_tag
def complete_tasks(user):
    return Task.complete.filter(assigned=user)

