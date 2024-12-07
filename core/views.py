from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.serializers import Serializer
from rest_framework.decorators import action

from .serializers import MovieSerializer, UserSerializer, UserRegistrationSerializer
from .models import Movie, User
from .permissions import IsAdminOrReadOnly, IsSelf

# Create your views here.

class MovieViewSet(ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    @action(['POST'], detail=True, url_path='make-favorite', permission_classes=[IsAuthenticated], serializer_class=Serializer)
    def make_favorite(self, request: Request, pk=None):
        user: User = request.user

        movie = get_object_or_404(Movie, pk=pk)
        user.favorite_movies.add(movie)
        user.save()

        return Response(status=204)
    
    @make_favorite.mapping.delete
    def unmake_favorite(self, request: Request, pk=None):
        user: User = request.user

        movie = get_object_or_404(Movie, pk=pk)
        user.favorite_movies.remove(movie)
        user.save()

        return Response(status=200)
    
    @action(['GET'], detail=False, permission_classes=[IsAuthenticated])
    def favorites(self, request: Request):
        user: User = request.user
        favorites = user.favorite_movies.all()
        content = {
            "user": UserSerializer(user, context={'request': request}).data,
            "movies": MovieSerializer(favorites, many=True, context={'request': request}).data
        }

        return Response(content, status=200)
    


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        
        return UserSerializer
    
    def get_permissions(self):
        if self.detail:
            return [(IsAdminUser | IsSelf)()]
        
        return [IsAdminUser()]
    
    def create(self, request: Request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        user_serializer = UserSerializer(serializer.save(), context={'request': request})

        return Response(user_serializer.data, status=201)
    

class ProfileViewSet(GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
    def list(self, request: Request):
        user: User = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request: Request):
        user: User = request.user
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()

        return Response(serializer.data, status=200)
    
    def delete(self, request: Request):
        user: User = request.user
        user.delete()
        return Response(status=204)
    
class RegisterView(GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request: Request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        user_serializer = UserSerializer(serializer.save(), context={'request': request})
        return Response(user_serializer.data, status=201)