from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models import User

class LogSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError({'email': 'Это поле обязательно.'})

        if not password:
            raise serializers.ValidationError({'password': 'Это поле обязательно.'})

        # Получаем пользователя по email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Неверный логин или пароль', code='invalid')

        # Аутентификация пользователя
        user = authenticate(username=user.username, password=password)

        if user is None:
            raise serializers.ValidationError('Неверный логин или пароль', code='invalid')

        # Добавляем username в данные
        data['username'] = user.username
        data['user'] = user
        return data