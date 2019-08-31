from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions, serializers, status, viewsets, mixins, views
from .models import User, Cat
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer, CatSerializer
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from oauth2_provider.models import ApplicationManager


from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import requests


CLIENT_ID = 'xyAVO54gS7hkX2h9OVybmO9oN4Nl9lhdF3YPsb5C'
CLIENT_SECRET = '4NPg2SJxpuyxfiXNWMMr66lJN7ImRHqyZFhrcdrgZTrBXRwk2g2Mrehd4xvgdv6ERnmmTn0rBPxmipG2pPFDnNytNtD0G6kJqY' \
                'rttaWaEgwVQ9f7HjHZrWcuqXcDNKAp'



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Registers user to the server. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    # Put the data from the request into the serializer
    serializer = CreateUserSerializer(data=request.data)
    # Validate the data
    if serializer.is_valid():
        # If it is valid, save the data (creates a user).
        serializer.save()
        # Then we get a token for the created user.
        # This could be done differentley
        r = requests.post('http://0.0.0.0:8000/o/token/',
            data={
                'grant_type': 'password',
                'username': request.data['username'],
                'password': request.data['password'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json(), status=r.status_code)
    return Response(serializer.errors)



@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
    'http://0.0.0.0:8000/o/token/',
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    print(r.status_code)
    return Response(r.json(), status=r.status_code)



@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    '''
    r = requests.post(
    'http://0.0.0.0:8000/o/token/',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json(), status=r.status_code)


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    r = requests.post(
        'http://0.0.0.0:8000/o/revoke_token/',
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    # If it goes well return sucess message (would be empty otherwise)
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    # Return the error if it goes badly
    return Response(r.json(), r.status_code)


# Create the API views
# class UserList(generics.ListCreateAPIView):
#     permission_classes = [AllowAny]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserList(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        print('TESTOV ', request.data)
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetails(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self, id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            raise Http404


    def get(self, request, id, *args, **kwargs):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id, *args, **kwargs):
        user = self.get_object(id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CatList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = CatSerializer

    def get_queryset(self):
        queryset = Cat.objects.all().filter(user_id=self.request.user.id)
        return queryset

    def post(self, request, format=None):
        serializer = CatSerializer(data=request.data, context={'user_id': self.request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CatDetails(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = CatSerializer

    def get_object(self, pk):
        try:
            return Cat.get_object_by_pk_for_user(pk=pk,user_id=self.request.user.id)
        except Cat.DoesNotExist:
            return '404'

    def get(self, request, pk, *args, **kwargs):
        cat = self.get_object(pk)
        if str(cat) == '403':
            return Response('403', status=status.HTTP_403_FORBIDDEN)
        elif str(cat) == '404':
            return Response('404', status=status.HTTP_404_NOT_FOUND)
        serializer = CatSerializer(cat)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        cat = self.get_object(pk)
        if str(cat) == '403':
            return Response('403', status=status.HTTP_403_FORBIDDEN)
        elif str(cat) == '404':
            return Response('404', status=status.HTTP_404_NOT_FOUND)

        serializer = CatSerializer(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cat = self.get_object(pk)
        if str(cat) == '403':
            return Response('403', status=status.HTTP_403_FORBIDDEN)
        elif str(cat) == '404':
            return Response('404', status=status.HTTP_404_NOT_FOUND)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





