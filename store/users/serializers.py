from rest_framework import serializers
from .models import CustomUser, Address

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number']
        read_only_fields = ['email', 'username']  

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'city', 'province', 'detailed_address', 'postal_code']
