from rest_framework.serializers import ModelSerializer
from tags.models import Tag

class DetailTagSerializer(ModelSerializer):
    
    class Meta:
        model = Tag
        fields = '__all__'

class CreateTagSerializer(ModelSerializer):
    
    class Meta:
        model = Tag
        fields = '__all__'