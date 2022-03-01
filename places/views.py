from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .permissions import *
from .models import *
from .serializers import *
from groups.serializers import *
from accounts.serializers import UserSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def retrieve(self, request, *args, **kwargs):
        if not Place.objects.filter(google_maps_id=kwargs['pk']).exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super().retrieve(request, *args, **kwargs)


class BasePlaceListViewSet(viewsets.ModelViewSet):
    
    def create_place(self, data):
        # DecimalField의 max_digits 속성을 맞추기 위해 위도, 경도 값의 자리수를 맞춰준다.
        for geometry in ['latitude', 'longitude']:
            data[geometry] = round(data[geometry], 10)
        
        place_serializer = PlaceSerializer(data=data)
        if place_serializer.is_valid(raise_exception=True):
            return place_serializer.save()


class PlaceListViewSet(BasePlaceListViewSet):
    queryset = PlaceList.objects.all()
    serializer_class = PlaceListSerializer
    permission_classes = [PlaceListPermission]

    def create(self, request):
        request.data['user'] = request.user.id
        return super().create(request)

    @action(detail=False, methods=['get'])
    def user(self, request):
        place_lists = request.user.place_lists.all()
        serializer = PlaceListSerializer(place_lists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            group_place = GroupPlace(place=place, place_list=place_list)
            group_place.save()
        else:
            group_place = place_list.places.get(place=google_maps_id)
        
        group_place.recommended_by.add(request.user)
        return Response(GroupPlaceListSerializer(place_list).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk):
        data = request.data
        google_maps_id = data['google_maps_id']

        group_place = GroupPlace.objects.get(place_list_id=pk, place_id=google_maps_id)
        group_place.recommended_by.remove(request.user.id)
        if len(group_place.recommended_by.all()) == 0:
            group_place.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_group_place_recommended_by(request, pk, google_maps_id):
    place_list = GroupPlaceList.objects.get(group_id=pk)
    group_place = place_list.places.get(place_id=google_maps_id)
    recommended_by = UserSerializer(group_place.recommended_by.all(), many=True)
    return Response(recommended_by.data, status.HTTP_200_OK)


'''
특정 장소를 저장한 PlaceList나 GroupPlaceList가 있는지 확인
'''
@api_view(['GET'])
def get_user_saved_place(request, google_maps_id):
    data = {
        'groups': [],
        'place_lists': [],
    }
    
    recommendeds = request.user.recommended.filter(place_id=google_maps_id)
    for recommended in recommendeds:
        data['groups'].append(recommended.place_list.group_id)
    
    for place_list in request.user.place_lists.all():
        if place_list.places.filter(google_maps_id=google_maps_id).exists():
            data['place_lists'].append(place_list.id)

    return Response(data, status=status.HTTP_200_OK)
