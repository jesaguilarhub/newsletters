from rest_framework.viewsets import ModelViewSet
from newsletters_app.models import Newsletter
from newsletters_app.serializers import NewsletterSerializer, DetailNewsletterSerializer, CreateNewsletterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from newsletters_app.permissions import CustomPermission
from copy import copy
from newsletters_app.tasks import send_email
from datetime import datetime, timedelta

class NewsletterViewSet(ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = (CustomPermission, )

    def create(self, request, *args, **kwargs):
        
        data = copy(request.data)
        data['created_by'] = request.user.id
        data['admins'] = request.user.id
        serializer = self.get_serializer_class()
        serialized  = serializer(data=data)
        
        if not serialized.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serialized.errors
            )
        serialized.save()
        return Response(
          status=status.HTTP_201_CREATED,
          data=serialized.data
        )

    def get_queryset(self):
                   
        try:
            if self.request.user.is_authenticated and self.request.user.is_staff:
                data = {}
            
                for k, v in self.request.query_params.items():
                    if k in ['page']:
                        continue
                    data[k] = v
                
                return self.queryset.filter(**data)  
            
            return self.queryset
                    
        except:
            return self.queryset

    def get_serializer_class(self):
        
        if self.action == 'list' and not self.request.user.is_staff:
            return NewsletterSerializer
        
        if self.action == 'retrieve' and self.request.user.is_staff:
            return DetailNewsletterSerializer
        
        if self.request.method == 'POST':
            return CreateNewsletterSerializer
        
        return NewsletterSerializer

    @action(methods=['PATCH'], detail=True)
    def vote(self, request, pk=None):
        newsletter = self.get_object()
        newsletter.votes.add(request.user)
        
        if newsletter.votes.all().count() == newsletter.target:
            newsletter.is_published = True
        
        newsletter.save()
         
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True)
    def subscribe(self, request, pk=None):
        newsletter = self.get_object()      
        newsletter.subs.add(request.user)
        send_email_datetime = datetime.now() + timedelta(days=newsletter.frequency)
        send_email.apply_async(eta=send_email_datetime)
        newsletter.save()

        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True)
    def unsubscribe(self, request, pk=None):
        newsletter = self.get_object()
        newsletter.subs.remove(request.user)
        newsletter.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=True)
    def invite(self, request, pk=None):
        newsletter = self.get_object()
        newsletter.admins.add(*request.data['admins'])
        newsletter.save()

        return Response(status=status.HTTP_201_CREATED)
    
    @action(methods=['PATCH'], detail=True)
    def edit(self, request, pk=None):
        newsletter = self.get_object()

        newsletter.name = request.data.get('name', newsletter.name)
        newsletter.description = request.data.get('description', newsletter.description)
        newsletter.frequency = request.data.get('frequency', newsletter.frequency)
        newsletter.target = request.data.get('target', newsletter.target)
        
        newsletter.save()
        return Response(status=status.HTTP_200_OK)