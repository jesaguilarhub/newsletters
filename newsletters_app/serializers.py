from rest_framework.serializers import ModelSerializer
from newsletters_app.models import Newsletter

class NewsletterSerializer(ModelSerializer):
       
    class Meta:
        model = Newsletter
        fields = ['nombre', 'id']

class CreateNewsletterSerializer(ModelSerializer):

    class Meta:
        model = Newsletter
        fields = '__all__'

class DetailNewsletterSerializer(ModelSerializer):

    class Meta:
        model = Newsletter
        fields = '__all__'
        lookup_field = 'slug'
        