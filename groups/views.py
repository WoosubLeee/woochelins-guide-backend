from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import GroupPermission
from groups.models import *
from groups.serializers import *


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [GroupPermission]

    def list(self, request):
        groups = request.user.groups.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = GroupSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            group = serializer.save()
            group.members.add(request.user)
            group.admin.add(request.user)
            return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
