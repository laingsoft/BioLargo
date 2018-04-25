from django.apps import AppConfig
from django.db.models.sql import Query
from .temp_fix import resolve_ref_temp_fix


class AnalyticsConfig(AppConfig):
    name = 'analytics'

    def ready(self):
        Query.resolve_ref = resolve_ref_temp_fix
