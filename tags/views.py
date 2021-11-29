from rest_framework.viewsets import ModelViewSet
from tags.models import Tag
from accounts.serializers import DetailTagSerializer, CreateTagSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = DetailTagSerializer
    permission_classes = (AllowAny,)

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
                return DetailTagSerializer
            
            if self.request.method == 'POST':
                return CreateTagSerializer