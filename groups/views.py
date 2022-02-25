from django.utils.crypto import get_random_string
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from .permissions import GroupPermission, GroupInvitationTokenPermission
from groups.models import *
from groups.serializers import *


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [GroupPermission]

    def create(self, request):
        data = request.data
        serializer = GroupSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            group = serializer.save()
            group.members.add(request.user)
            group.admin.add(request.user)
            return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def user(self, request):
        groups = request.user.groups.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add(self, request, pk):
        token = request.data['token']
        group = Group.objects.get(id=pk)
        if group.validate_not_in_group(request, pk) and group.validate_token(pk, token):
            group.members.add(request.user.id)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def is_admin(self, request, pk):
        if request.user in Group.objects.get(id=pk).admin.all():
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([GroupInvitationTokenPermission])
def create_token(request, pk):
    if request.user in Group.objects.get(id=pk).admin.all():
        token = get_random_string(length=32)
        data={
            'group': pk,
            'token': token
        }
        serializer = GroupInvitationTokenSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    else:
        return Response('해당 모임의 관리자가 아닙니다.', status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def validate_invitation(request, pk, token):
    group = Group.objects.get(id=pk)
    if not group.validate_not_in_group(request, pk):
        return Response({
            'has_joined': True,
            'detail': '이미 초대된 사용자입니다.',
        }, status.HTTP_400_BAD_REQUEST)
    elif not group.validate_token(pk, token):
        return Response({
            'has_joined': False,
            'valid_token': False,
            'detail': 'The token is invalid.',
        }, status.HTTP_403_FORBIDDEN)
    return Response({
        'groud_name': group.name,
    },status=status.HTTP_202_ACCEPTED)