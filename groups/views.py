from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import *
from .permissions import *
from places.models import Place, GroupPlace


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [GroupPermission]

    def create(self, request):
        data = request.data
        data['admins'] = [request.user.id]
        serializer = GroupSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            group = serializer.save()
            group.members.add(request.user.id)
            return Response(GroupSerializer(group).data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
                
    @action(detail=False, methods=['get'])
    def user(self, request):
        groups = request.user.groups.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'])
    def token(self, request, pk):
        group = get_object_or_404(Group, id=pk)
        if request.method == 'GET':
            token = request.query_params['token']
            if not group.is_user_in_group(request, pk):
                if group.is_token_valid(pk, token):
                    return Response(GroupSerializer(group).data, status=status.HTTP_200_OK)
                return Response({'message': '유효하지 않은 토큰입니다.'}, status.HTTP_400_BAD_REQUEST)
            return Response({'message': '이미 가입한 모임입니다.'}, status.HTTP_400_BAD_REQUEST)
        elif request.method == 'POST':
            if request.user in group.admins.all():
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
            return Response({'message': '해당 모임의 관리자가 아닙니다.'}, status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['post'])
    def member(self, request, pk):
        if request.method == 'POST':
            token = request.query_params['token']
            group = get_object_or_404(Group, id=pk)
            if not group.is_user_in_group(request, pk):
                if group.is_token_valid(pk, token):
                    group.members.add(request.user.id)
                    return Response(status=status.HTTP_201_CREATED)
                return Response({'message': '유효하지 않은 토큰입니다.'}, status.HTTP_400_BAD_REQUEST)
            return Response({'message': '이미 가입한 모임입니다.'}, status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'])
    def place(self, request, pk):
        group = get_object_or_404(Group, id=pk)
        # 맛집 Group 추천 places에 추가
        if request.method == 'POST':
            data = request.data
            kakao_map_id = data['kakao_map_id']
            
            place, created = Place.objects.get_or_create(
                kakao_map_id=kakao_map_id,
                defaults=data
            )
            group_place, created = GroupPlace.objects.get_or_create(place=place, group=group)
            group_place.recommenders.add(request.user)
            group.places.add(group_place)
            return Response(GroupSerializer(group).data, status.HTTP_201_CREATED)
        
        # 맛집 Group 추천 places에서 제거
        elif request.method == 'DELETE':
            group_place = GroupPlace.objects.get(group_id=group.id, place_id=request.query_params['kakao_map_id'])
            group_place.recommenders.remove(request.user.id)
            if len(group_place.recommenders.all()) == 0:
                group_place.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(GroupPlaceSerializer(group_place).data, status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def is_admin(self, request, pk):
        if request.user in Group.objects.get(id=pk).admins.all():
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_200_OK)