from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import LoginSerializer

class LoginView(APIView):
    @staticmethod
    def post(request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Создание токенов JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Установка куки
            response = Response({
                'success': True,
                'access_token': access_token,
                'refresh_token': str(refresh),
                'user_id': user.id  # Отправляем только ID пользователя
            }, status=status.HTTP_200_OK)
            response.set_cookie('access_token', access_token, httponly=True)
            response.set_cookie('refresh_token', str(refresh), httponly=True)

            return response
        else:
            if 'non_field_errors' in serializer.errors:
                return Response({'detail': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)