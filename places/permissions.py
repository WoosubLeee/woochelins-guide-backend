from rest_framework import permissions


class GroupPlacePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user in obj.group.members.all()


class MyListPermission(permissions.BasePermission):
    message = '해당 유저의 리스트가 아닙니다.'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user        