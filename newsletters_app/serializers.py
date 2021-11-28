from rest_framework.serializers import ModelSerializer
from newsletters_app.models import Newsletter

class NewsletterSerializer(ModelSerializer):
       
    class Meta:
        model = Newsletter
        fields = '__all__'

class CreateNewsletterSerializer(ModelSerializer):

    class Meta:
        model = Newsletter
        fields = '__all__'

class DetailNewsletterSerializer(ModelSerializer):

    class Meta:
        model = Newsletter
        fields = '__all__'
        