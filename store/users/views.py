
from django.db import transaction
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .serializers import CustomTokenObtainPairSerializer
import random
from django.core.cache import cache
from datetime import timedelta
User = get_user_model()


# Helper function to generate OTP
def generate_otp(email, **kwargs):

    if cache.get(email):
        return False
    # otp = random.randint(100000, 999999)
    # otp_str = str(otp)
    kwargs['otp'] = "0000"
    cache.set(email, kwargs, timeout=300)

    return True


class RegisterView(APIView):
    def post(self, request):

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password or not email:
            raise ValidationError("Username, email, and password are required.")
        
        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "Invalid email address."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
      
        generate_otp(email, username=username,password=password, register=True)
        
        return Response({"message": "send the code we emailed you"}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        if not email or not otp:
            raise ValidationError("Email and OTP are required.")

        cached_value = cache.get(email)
        if not cached_value or str(cached_value["otp"]) != str(otp):
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
        cache.delete(email)
        if cached_value.get("register") == True:
            user = User.objects.create_user(phone_number="0900000000",
                email=email, password=cached_value["password"], username=cached_value["username"])
        else:
            user = User.objects.get(email=email)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "message": "User registered and logged in successfully!",
            "access": access_token,
            "refresh": refresh_token
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
