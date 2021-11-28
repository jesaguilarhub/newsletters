from rest_framework.permissions import BasePermission

class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not request.user.is_staff and view.action == 'create':
            return False
        
        if not request.user.is_staff and view.action == 'edit':
            return False
        
        if not request.user.is_staff and view.action == 'invite':
            return False 
        
        if request.user.is_staff and view.action == 'vote':
            return False

        if request.user.is_staff and view.action == 'subscribe':
            return False
        
        if request.user.is_staff and view.action == 'unsubscribe':
            return False
        
        return True
    
    def has_object_permission(self, request, view, newsletter):
        if view.action == 'edit' and request.method == 'PATCH' and request.user in newsletter.admins.all():
            return True

        if view.action == 'unsubscribe' and request.method == 'POST' and request.user in newsletter.subs.all():
           return True 

        if view.action == 'invite' and request.method == 'POST' and request.user in newsletter.admins.all():
            return True

        if view.action == 'subscribe' and request.method == 'POST' and newsletter.is_published:
            return True

        if view.action == 'vote' and request.method == 'PATCH' and not request.user.is_staff:
            return True
            
        return False