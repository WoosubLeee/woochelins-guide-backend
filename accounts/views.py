from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import *
from .permissions import *
from places.serializers import MyListSerializer


User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
            
        my_list_serializer = MyListSerializer(data={
            'name': '나의 맛집 리스트',
            'user': user.id,
            'is_default': True,
        })
        if my_list_serializer.is_valid(raise_exception=True):
            my_list_serializer.save()
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(my_list_serializer.data, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        }, status.HTTP_201_CREATED)


@api_view(['POST'])
def validate(request):
    if request.user.is_authenticated:
        return Response('The user is authenticated.', status=status.HTTP_200_OK)
    return Response('The user is not authenticated', status=status.HTTP_401_UNAUTHORIZED)
    