from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import FloatField
from django.db.models.functions import Cast


def json_field_format(field_name):
    return {field_name:
                KeyTextTransform(
                    field_name,
                    'experimentData')}


def json_field_arrayAgg(field_name):
    return {field_name: ArrayAgg(Cast(
                KeyTextTransform(
                    field_name,
                    'experimentData'),
                FloatField()))}

def isNum(n):
    try:
        float(n)
    except ValueError:
        return False

    return True
