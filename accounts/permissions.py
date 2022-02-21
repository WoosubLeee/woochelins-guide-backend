from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    message = '권한이 없습니다.'
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
