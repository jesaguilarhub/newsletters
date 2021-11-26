from rest_framework.viewsets import ModelViewSet
from newsletters_app.models import Newsletter
from newsletters_app.serializers import NewsletterSerializer, DetailNewsletterSerializer, CreateNewsletterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from newsletters_app.permissions import CustomPermission
from copy import copy
from django.contrib.auth import User


class NewsletterViewSet(ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = DetailNewsletterSerializer
    permission_classes = (CustomPermission, )

    def create(self, request, *args, **kwargs):
        
        data = copy(self.request.data)
        data['created_by'] = self.request.user.id
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
    
    def partial_update(self, request, pk=None):

        if not self.request.user.is_staff:
          return Response(status=status.HTTP_400_BAD_REQUEST)
        
        newsletter = self.get_object()
        data = request.data
        ids = []
        for obj in data:
            ids.add(obj.id)

        newsletter.subs.add(User.objects.filter(id__in=ids))
        newsletter.save()
        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):
                   
        try:
            if self.request.user.is_authenticated and not self.request.user.is_staff:

                self.queryset = self.queryset.filter(subs__id=self.request.user.id)

            return self.querySet           
        except:
            return self.queryset

    def get_serializer_class(self):
        
        if self.action == 'list' and not self.request.user.is_staff:
            return DetailNewsletterSerializer
        
        if self.action == 'retrieve' and self.request.user.is_staff:
            return DetailNewsletterSerializer
        
        if self.request.method == 'POST':
            return CreateNewsletterSerializer
        
        return DetailNewsletterSerializer

    @action(methods=['PATCH'], detail=True)
    def vote(self, request, pk=None):
        newsletter = self.get_object()
        if newsletter.votes.filter(user__id=request.user.id).exists() or request.user.is_staff:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        newsletter.votes.add(User.objects.get(id=request.user.id))

        if newsletter.votes.all().count() == newsletter.target:
            newsletter.is_published = True
        
        newsletter.save()
         
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['POST', 'DELETE'], detail=True)
    def subscribe(self, request, pk=None):
      newsletter = self.get_object()
      if not newsletter.is_published:
          return Response(status=status.HTTP_400_BAD_REQUEST)
      
      newsletter.subs.add(User.objects.get(id=request.user.id))
      newsletter.save()

      return Response(status=status.HTTP_201_CREATED)
