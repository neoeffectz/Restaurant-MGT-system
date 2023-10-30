from rest_framework import permissions


# Used the custom drf permisions to access various groups
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="Manager"):
            return True
        return False 
    

class IsAttendant(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="Attendants"):
            return True
        return False 
    
    
    
