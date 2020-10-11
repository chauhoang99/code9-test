from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate(self, attrs):
        email = User.objects.filter(email=attrs['email'])
        if email:
            raise exceptions.ValidationError({'email': 'A user with this email already exists.'})
        else:
            return attrs

    def create(self, validated_data):
        user = User()
        user.username = validated_data['username']
        user.email = validated_data['email']
        user.set_password(validated_data['password'])
        user.save()

        # Can add email verification send out function in post_save signal of User
        return validated_data


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, attr):
        return attr.strip().lower()

    def validate(self, attrs):
        if not attrs.get('username') and not attrs.get('password'):
            raise exceptions.ValidationError('need username')
        return attrs

    def authenticate(self):
        data = self.validated_data
        print(data)
        user = authenticate(**data)
        return user


class ShapeSerializer(serializers.Serializer):
    coords = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField()
        )
    )
