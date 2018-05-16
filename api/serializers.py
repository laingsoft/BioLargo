from app.models import *
from accounts.models import User
from rest_framework import serializers
from project_management.models import Task
from SOP.models import SOP
from inventory.models import Item
import base64
from django.core.files import File

class imageSerializer(serializers.ModelSerializer):
    base64_image = serializers.SerializerMethodField()

    class Meta:
        model = ExperimentImages
        fields = ['id', 'base64_image']

    def get_base64_image(self, obj):
        f = open(obj.photo.path, 'rb')
        image = File(f)
        data = base64.b64encode(image.read())
        f.close()
        return data

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'company', 'first_name', 'last_name',
            'email', 'is_manager', "last_login"]

class commentSerializer(serializers.ModelSerializer):
    user = userSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

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

class experimentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentData
        fields = ['experimentData', 'experiment']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ('company', 'timestamp')


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

class notificationSerializer(serializers.ModelSerializer):
    subject = userSerializer()
    class Meta:
        model = Notification
        fields = '__all__'



class SimpleProjectSerializer(serializers.ModelSerializer):
    """
    only serializes id and name. No extra information provided. Used by
    website.
    """
    class Meta:
        model = Project
        fields = ('id', 'name')

class SimpleUserSerializer(serializers.ModelSerializer):
    """
    returns a name or email and an id
    """
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'email')

    def get_name(self, obj):
        return obj.get_full_name()


class SimpleSOPSerializer(serializers.ModelSerializer):
    class Meta:
        model = SOP
        fields = ('name', 'id')


class SimpleTaskSerializer(serializers.ModelSerializer):
    project = SimpleProjectSerializer()
    sop = SimpleSOPSerializer()

    class Meta:
        model = Task
        exclude = ('company', 'timestamp')
        
class SimpleExperimentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentData
        fields = ["id","experiment"]
    
class experimentDataAnnotationSerializer(serializers.ModelSerializer):
    experimentData = SimpleExperimentDataSerializer()
    user = SimpleUserSerializer()
    class Meta:
        model = ExperimentDataAnnotation
        fields = '__all__'
        
class SimpleInventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["name",'description']
