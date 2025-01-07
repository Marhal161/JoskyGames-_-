from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                print(f"Authentication failed for email: {email}")  # Отладочное сообщение
                print(f"Authentication failed for password: {password}")  # Отладочное сообщение
                raise serializers.ValidationError('Неверный логин или пароль')
        else:
            raise serializers.ValidationError('Обязательные поля не заполнены')

        data['user'] = user
        return data

