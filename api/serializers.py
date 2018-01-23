from app.models import *
from accounts.models import User
from rest_framework import serializers

class commentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'company', 'first_name', 'last_name', 
            'email', 'is_manager']

class experimentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentData
        fields = ['experiment','experimentData']
        
class experimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'

class groupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class tagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class projectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'