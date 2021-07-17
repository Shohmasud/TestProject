from rest_framework import serializers
from .models import *
class serialiaersfileName(serializers.ModelSerializer):
    class Meta:
        model = fileName
        fields = ('name_file',)

class sResponse(serializers.ModelSerializer):
    class Meta:
        model = response
        fields = '__all__'