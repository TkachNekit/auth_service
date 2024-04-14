from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from users.authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from users.models import User, RefreshToken
from users.serializers import UserSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data['email']).first()

        if not user:
            raise APIException('Invalid credentials!')

        if not user.check_password(request.data['password']):
            raise APIException('Invalid credentials!')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        RefreshToken.revoke_all_tokens(user)  # Revoke all tokens for the user
        RefreshToken.objects.create(jti=refresh_token, user=user)

        response = Response()

        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return response


class UserAPIView(APIView):
    def get(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            user = User.objects.filter(id=id).first()
            data = UserSerializer(user).data
            data.pop('password')
            data['username'] = "" if data['username'] is None else data['username']
            return Response(data)

        raise AuthenticationFailed('Unauthenticated')

    def put(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            user = User.objects.filter(id=id).first()
            serializer = UserSerializer(data=request.data, instance=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        raise AuthenticationFailed('Unauthenticated')


class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.data['refresh_token']
        id = decode_refresh_token(refresh_token)
        user = User.objects.filter(id=id).first()

        RefreshToken.revoke_all_tokens(user)  # Revoke all tokens for the user
        access_token = create_access_token(id)
        new_refresh_token = create_refresh_token(id)

        return Response({
            'access_token': access_token,
            'refresh_token': new_refresh_token
        })


class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data['refresh_token']
        id = decode_refresh_token(refresh_token)
        user = User.objects.filter(id=id).first()

        RefreshToken.revoke_all_tokens(user)  # Revoke all tokens for the user
        return Response({'success': 'User logged out.'})
