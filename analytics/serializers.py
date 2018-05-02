from .models import Session, Action
from rest_framework import serializers
from app.models import Experiment
from project_management.models import Project


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'name', 'project')


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ('id', 'friendly_name', 'create_timestamp')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name')