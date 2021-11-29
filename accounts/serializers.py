from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

class DetailAccountSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

class CreateAccountSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'is_staff']