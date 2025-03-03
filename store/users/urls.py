from django.urls import path
from .views import RegisterView,VerifyOTPView,UserInfoView,PasswordResetView,AddressUpdateView,UserAddressesView,UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView ,TokenVerifyView,TokenRefreshView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), 
    path('login/', TokenObtainPairView.as_view(), name='login'), 
    path('otp/', VerifyOTPView.as_view(), name='otp'),
    path('verify/', TokenVerifyView.as_view(), name='verify'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('user-info/',UserInfoView.as_view(), name='user-info'),
    path('reset-password/',PasswordResetView.as_view(), name='rest-password'),
    path("profile/", UserProfileView.as_view() , name="profile"),
    path('addresses/', UserAddressesView.as_view(), name='user-addresses'),
    path('addresses/<int:pk>/', AddressUpdateView.as_view(), name='address-update'),
]
