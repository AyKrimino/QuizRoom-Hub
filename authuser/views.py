from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from datetime import datetime
from datetime import timezone

from .serializers import RegisterUserSerializer, LoginUserSerializer, ErrorResponseSerializer

User = get_user_model()


class RegisterUserView(APIView):
    """
    API view to handle user registration.

    This view allows users to register by creating a new user account. It handles
    the registration process, including validation of user data, password confirmation,
    and user creation. The registration requires that the email is unique and that
    both password fields match.

    Permissions:
        - `AllowAny`: No authentication is required; the endpoint is open to everyone.

    Methods:
        post(request, *args, **kwargs):
            Handles POST requests to register a new user. Validates the provided
            data using `RegisterUserSerializer`, creates the user if the data is valid,
            and returns the user data in the response.

    Request:
        - `RegisterUserSerializer`: Expected request data for user registration.

    Responses:
        - `201 Created`: Successfully created user, returns user data.
        - `400 Bad Request`: Invalid request data, returns error details.

    Raises:
        - `ValidationError`: If the provided data is invalid, such as mismatched passwords.
    """
    permission_classes = (AllowAny,)

    @extend_schema(
        request=RegisterUserSerializer,
        responses={
            201: RegisterUserSerializer,
            400: OpenApiResponse(ErrorResponseSerializer, description="Bad Request")
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new user.

        Validates the provided data, ensuring that the email is unique and the passwords
        match. If valid, creates a new user and returns the user data. If the data is invalid,
        returns error details.

        Args:
            request (Request): The HTTP request object containing user registration data.

        Returns:
            Response: The response containing the created user details or error information.

        Raises:
            ValidationError: If the data provided for registration is invalid, such as
            passwords not matching or email not being unique.
        """
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    """
    API view to handle user login.

    This view allows users to log in by providing their email and password. It validates
    the credentials, updates the user's last login timestamp, and generates JWT tokens for
    authentication. Successful login returns the user data along with the tokens.

    Permissions:
        - `AllowAny`: No authentication is required; the endpoint is open to everyone.

    Methods:
        post(request, *args, **kwargs):
            Handles POST requests to log in a user. Validates the provided credentials using
            `LoginUserSerializer`, updates the last login timestamp, generates JWT tokens,
            and returns the user data along with tokens.

    Request:
        - `LoginUserSerializer`: Expected request data for user login, including email and password.

    Responses:
        - `200 OK`: Successful login, returns user data and JWT tokens.
        - `400 Bad Request`: Invalid request data, returns error details.
        - `401 Unauthorized`: Invalid credentials, returns error details.

    Raises:
        - `ValidationError`: If the credentials provided are invalid or if the user cannot be authenticated.
    """
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
        """
        Handles POST requests to log in a user.

        Validates the provided credentials and, if valid, updates the user's last login
        timestamp, generates JWT tokens, and returns the user data along with the tokens.

        Args:
            request (Request): The HTTP request object containing user login data.

        Returns:
            Response: The response containing the user data and JWT tokens or error information.

        Raises:
            ValidationError: If the provided credentials are invalid or if the user cannot be authenticated.
        """
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.last_login = datetime.now(tz=timezone.utc)
        user.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class LogoutUserView(APIView):
    """
    API view to handle user logout.

    This view allows users to log out by invalidating their refresh token. The refresh token
    is added to a blacklist, effectively logging out the user by preventing the issuance of
    new access tokens using that refresh token.

    Permissions:
        - `IsAuthenticated`: The user must be authenticated to access this view.

    Methods:
        post(request, *args, **kwargs):
            Handles POST requests to log out a user. Invalidates the provided refresh token
            by adding it to a blacklist.

    Request:
        - `LoginUserSerializer`: Expected request data should include a refresh token.

    Responses:
        - `205 Reset Content`: Successfully invalidated the refresh token.
        - `400 Bad Request`: Invalid request data or error during token processing.

    Raises:
        - `Exception`: If there is an error processing the refresh token or if the token is invalid.
    """
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=LoginUserSerializer,  # The request body is expected to have a refresh token
        responses={
            205: OpenApiResponse(description="Reset Content"),
            400: OpenApiResponse(ErrorResponseSerializer, description="Bad Request")
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to log out a user.

        Invalidates the provided refresh token by adding it to a blacklist. This prevents
        the issuance of new access tokens using the provided refresh token.

        Args:
            request (Request): The HTTP request object containing the refresh token.

        Returns:
            Response: The response indicating whether the logout was successful or if there was an error.

        Raises:
            Exception: If there is an issue processing the refresh token or if the token is invalid.
        """
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
