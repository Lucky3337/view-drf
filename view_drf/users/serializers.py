from rest_framework import serializers
from .models import User, Cat


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username',)
        read_only_fields = ('username', )

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.save()
        return instance


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', )
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = ('pk', 'created', 'nickname', 'mass', 'age', 'breed', 'hair', 'user')
        read_only_fields = ('pk', 'user', 'created')


    def create(self, validated_data, *args, **kwargs):
        """
        Create and return a new `Cat` instance, given the validated data.
        """

        cat = Cat(
            nickname = validated_data['nickname'],
            mass=validated_data['mass'],
            age=validated_data['age'],
            breed=validated_data['breed'],
            hair=validated_data['hair'],
            user_id=self.context['user_id']
        )
        cat.save()
        return cat
