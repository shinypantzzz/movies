from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request: Request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    
class IsSelf(BasePermission):
    def has_object_permission(self, request: Request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user == obj