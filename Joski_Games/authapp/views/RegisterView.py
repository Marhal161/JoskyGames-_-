from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import RegisterSerializer  # Импорт сериализатора
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

class RegisterView(APIView):
    @staticmethod
    def post(request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()

                # Создание токенов JWT
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Установка куки
                response = HttpResponseRedirect('/')
                response.set_cookie('access_token', access_token, httponly=True)
                response.set_cookie('refresh_token', str(refresh), httponly=True)
                response.status_code = status.HTTP_201_CREATED  # Установка статус кода 201

                # Возвращение ответа
                return response
            except Exception as e:  # Обработка исключений
                return Response({
                    'success': False,
                    'message': 'Ошибка при создании пользователя: {}'.format(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'success': False,
            'message': 'Validation errors',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class RegisterFView(View):
    def get(self, request):
        return render(request, 'register.html')