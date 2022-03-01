from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .permissions import *
from .serializers import UserSerializer, CustomAuthTokenSerializer
from places.serializers import PlaceListSerializer
from groups.serializers import GroupSerializer


User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if not User.objects.filter(email=request.data['email']).exists():
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            
            place_list_serializer = PlaceListSerializer(data={
                'name': '나의 맛집',
                'user': user.id,
                'is_default': True,
            })
            if place_list_serializer.is_valid(raise_exception=True):
                place_list_serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({
        'email_exists': True,
        'detail': 'A user with the email already exists.'
    }, status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


@api_view(['POST'])
def is_valid(request):
    if request.user.is_authenticated:
        return Response('The user is authenticated.', status=status.HTTP_200_OK)
    return Response('The user is not authenticated', status=status.HTTP_401_UNAUTHORIZED)
    