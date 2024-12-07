from rest_framework.serializers import HyperlinkedModelSerializer, Serializer, CharField

from .models import Movie, User

class UserSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email']

class UserRegistrationSerializer(Serializer):
    user = UserSerializer(required=True)
    password = CharField(required=True, allow_blank=False, max_length=255)

    def create(self, validated_data):
        user = User.objects.create(**validated_data['user'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class MovieSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ['url', 'id', 'title', 'description']
        
        