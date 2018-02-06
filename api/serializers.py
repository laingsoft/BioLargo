from app.models import *
from accounts.models import User
from rest_framework import serializers

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'company', 'first_name', 'last_name', 
            'email', 'is_manager']

class commentSerializer(serializers.ModelSerializer):
    user = userSerializer()
    class Meta:
        model = Comment
        fields = ['experiment', 'content', 'user']

class experimentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentData
        fields = ['experimentData']
        
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

class experimentSerializer(serializers.ModelSerializer):
    tags = tagsSerializer(many=True)
    project = projectSerializer()
    user = userSerializer()
    class Meta:
        model = Experiment
        fields = '__all__'

class simpleExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'

#here, Fields referes to the model fields that the templates use
class fieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fields
        fields = '__all__'

class templateSerializer(serializers.ModelSerializer):
    fields = fieldSerializer(many=True)
    metadata = fieldSerializer(many=True)
    class Meta:
        model = Template
        fields = '__all__'
