from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from accounts.serializers import DetailAccountSerializer, CreateAccountSerializer
from rest_framework.response import Response
from rest_framework import status

class AccountViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = DetailAccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serialized  = serializer(data=request.data)

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

    def get_serializer_class(self):
                       
            if self.action == 'retrieve' and self.request.user.is_staff:
                return DetailAccountSerializer
            
            if self.request.method == 'POST':
                return CreateAccountSerializer
