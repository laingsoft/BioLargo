from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import FloatField
from django.db.models.functions import Cast


def json_field_format(field_name):
    return {field_name: Cast(
                KeyTextTransform(
                    field_name,
                    'experimentData'),
                FloatField())}


def json_field_arrayAgg(field_name):
    return {field_name: ArrayAgg(Cast(
                KeyTextTransform(
                    field_name,
                    'experimentData'),
                FloatField()))}
