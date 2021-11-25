from rest_framework.permissions import BasePermission

class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not request.user.is_staff and view.action == 'create':
            return False
        
        if not request.user.is_staff and view.action == 'partial_update':
            return False
        
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if view.action == 'vote' and request.method in ['DELETE', 'PATCH', 'PUT'] and obj.created_by == request.user:
           return True 

        return False