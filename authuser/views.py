from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterUserSerializer, LoginUserSerializer, ErrorResponseSerializer

User = get_user_model()


class RegisterUserView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=RegisterUserSerializer,
        responses={
            201: RegisterUserSerializer,
            400: OpenApiResponse(ErrorResponseSerializer, description="Bad Request")
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=LoginUserSerializer,
        responses={
            200: OpenApiResponse(LoginUserSerializer, description="Successful login"),
            400: OpenApiResponse(ErrorResponseSerializer, description="Bad Request"),
            401: OpenApiResponse(ErrorResponseSerializer, description="Unauthorized")
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class LogoutUserView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=LoginUserSerializer,  # The request body is expected to have a refresh token
        responses={
            205: OpenApiResponse(description="Reset Content"),
            400: OpenApiResponse(ErrorResponseSerializer, description="Bad Request")
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
