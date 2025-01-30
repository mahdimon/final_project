
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import random
from django.core.cache import cache
from .tasks import send_otp_email
from rest_framework import status, generics
from .models import Address
from .serializers import UserProfileSerializer, AddressSerializer
User = get_user_model()


# Helper function to generate OTP
def generate_otp(email, **kwargs):

    if cache.get(email):
        return False
    # otp = random.randint(100000, 999999)
    # otp_str = str(otp)
    kwargs['otp'] = "0000"
    cache.set(email, kwargs, timeout=300)
    send_otp_email.delay(email, kwargs['otp'])

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
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)
      
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
            user.set_password(cached_value["password"])
            user.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            "message": "User registered and logged in successfully!",
            "access": access_token,
            "refresh": refresh_token
        }, status=status.HTTP_201_CREATED)

        
 
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
        }) 
 
 
class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)

    
        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        generate_otp(email, password=new_password)

        return Response({"message": "Proceed to OTP validation."}, status=status.HTTP_200_OK)
       


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Fetch User Addresses

class UserAddressesView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

# Update Address
class AddressUpdateView(generics.UpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        try:
            address = Address.objects.get(id=pk, customer=request.user)
        except Address.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
