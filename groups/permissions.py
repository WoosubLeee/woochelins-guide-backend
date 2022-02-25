from rest_framework import permissions


class GroupPermission(permissions.BasePermission):
    message = '해당 유저의 리스트가 아닙니다.'

    def has_permission(self, request, view):
        return request.user.is_authenticated


class GroupInvitationTokenPermission(permissions.BasePermission):
    message = '권한이 없습니다.'

    def has_permission(self, request, view):
        return request.user.is_authenticated