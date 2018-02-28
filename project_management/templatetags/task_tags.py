from django import template
from project_management.models import Task

register = template.Library()


@register.simple_tag
def incomplete_tasks(user):
    """
    gets a user's incomplete tasks
    """
    return Task.incomplete.filter(assigned=user)


@register.simple_tag
def task_progress(project):
    """
    calculates progress percentage. complete / total
    """
    complete = Task.objects.filter(project=project, status='C').count()
    total = Task.objects.filter(project=project).count()
    if total == 0:
        return 0

    return round(complete/total * 100, 2)


@register.simple_tag
def count_scientists(project):
    """
    counts the number of scientists working on a project.
    """
    return project.experiment_set.all().distinct('user').count()


@register.simple_tag
def get_tags(project):
    return project.experiment_set.all().values('tags').distinct('tags')
