from rest_framework.permissions import BasePermission

class IsSuperuserOrStaff(BasePermission):
    """
    Custom permission to allow access only to superusers or staff users.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.is_staff)

class IsSuperuserOnly(BasePermission):
    """
    Custom permission to allow access only to superusers.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser