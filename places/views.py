from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import *


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def create(self, request, *args, **kwargs):
        place, created = Place.objects.update_or_create(
            kakao_map_id=request.data['kakao_map_id'],
            defaults=request.data
        )
        return Response(PlaceSerializer(place).data, status.HTTP_200_OK)


class GroupPlaceViewSet(viewsets.ModelViewSet):
    queryset = GroupPlace.objects.all()
    serializer_class = GroupPlaceSerializer
    permission_classes = [GroupPlacePermission]


class MyListViewSet(viewsets.ModelViewSet):
    queryset = MyList.objects.all()
    serializer_class = MyListSerializer
    permission_classes = [MyListPermission]

    def create(self, request):
        request.data['user'] = request.user.id
        return super().create(request)

    @action(detail=True, methods=['post', 'delete'])
    def place(self, request, pk):
        my_list = get_object_or_404(MyList, id=pk)
        # 맛집 MyList에 추가
        if request.method == 'POST':
            data = request.data
            kakao_map_id = data['kakao_map_id']

            place = Place.objects.get_or_create(
                kakao_map_id=kakao_map_id,
                defaults=data,
            )

            my_list.places.add(kakao_map_id)
            return Response(MyListSerializer(my_list).data, status.HTTP_201_CREATED)

        # 맛집 MyList에서 제거
        elif request.method == 'DELETE':
            try:
                my_list.places.remove(request.query_params['kakao_map_id'])
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({'message': '맛집이 정상적으로 제거되지 않았습니다.'}, status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def user(self, request):
        if 'default' in request.query_params and int(request.query_params['default']):
            my_list = request.user.my_lists.get(is_default=True)
            return Response(MyListSerializer(my_list).data, status.HTTP_200_OK)

        my_lists = request.user.my_lists.all()
        serializer = MyListSerializer(my_lists, many=True)
        return Response(serializer.data, status.HTTP_200_OK)