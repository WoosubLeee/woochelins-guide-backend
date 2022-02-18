from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .permissions import *
from places.models import *
from places.serializers import *
from groups.serializers import *


class BasePlaceListViewSet(viewsets.ModelViewSet):
    
    def create_place(self, data):
        place_data = {k: data[k] for k in ['google_maps_id', 'name']}
        for geometry in ['latitude', 'longitude']:
            place_data[geometry] = round(data[geometry], 10)
        place_serializer = PlaceSerializer(data=place_data)
        if place_serializer.is_valid(raise_exception=True):
            return place_serializer.save()


class PlaceListViewSet(BasePlaceListViewSet):
    queryset = PlaceList.objects.all()
    serializer_class = PlaceListSerializer
    permission_classes = [PlaceListPermission]

    def list(self, request):
        place_lists = request.user.place_lists.all()
        serializer = PlaceListSerializer(place_lists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        request.data['user'] = request.user.id
        return super().create(request)

    @action(detail=True, methods=['post'])
    def add(self, request, pk):
        data = request.data

        google_maps_id = data['google_maps_id']
        if not Place.objects.filter(google_maps_id=google_maps_id).exists():
            self.create_place(data)

        place_list = PlaceList.objects.get(id=pk)
        place_list.places.add(google_maps_id)
        return Response(PlaceListSerializer(place_list).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk):
        data = request.data
        place_list = PlaceList.objects.get(id=pk)
        place_list.places.remove(data['google_maps_id'])
        return Response('Place removed from Place List successfully.', status=status.HTTP_204_NO_CONTENT)
        

@api_view(['GET'])
def get_user_default_list(request):
    place_list = request.user.place_lists.get(is_default=True)
    return Response(PlaceListSerializer(place_list).data, status=status.HTTP_200_OK)


class GroupPlaceListViewSet(BasePlaceListViewSet):
    queryset = GroupPlaceList.objects.all()
    serializer_class = GroupPlaceListSerializer
    permission_classes = [GroupPlaceListPermission]

    # GroupPlace 추가, recommended_by에 추가
    @action(detail=True, methods=['post'])
    def add(self, request, pk):
        data = request.data
        google_maps_id = data['google_maps_id']

        place_list = GroupPlaceList.objects.get(group_id=pk)
        '''
        GroupPlaceList에 이미 추가된 GroupPlace인지 확인하여
        없다면 생성, 있다면 가져오기
        '''
        if not place_list.places.filter(place=google_maps_id).exists():
            '''
            이미 생성된 Place인지 확인하여
            없다면 생성, 있다면 가져오기
            '''
            if not Place.objects.filter(google_maps_id=google_maps_id).exists():
                place = self.create_place(data)
            else:
                place = Place.objects.get(google_maps_id=google_maps_id)
            
            '''
            이미 생성된 GroupPlace인지 확인하여
            없다면 생성, 있다면 가져오기
            '''
            group_place_data = {
                'place': place.google_maps_id,
                'place_list': place_list,
            }
            group_place_serializer = GroupPlaceSerializer(data=group_place_data)
            if group_place_serializer.is_valid(raise_exception=True):
                group_place = group_place_serializer.save()
        else:
            group_place = place_list.places.get(place=google_maps_id)
        
        group_place.recommended_by.add(request.user)
        return Response(GroupPlaceListSerializer(place_list).data, status=status.HTTP_201_CREATED)
