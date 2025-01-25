from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView,VerifyOTPView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), 
    path('login/', CustomTokenObtainPairView.as_view(), name='login'), 
    path('otp/', VerifyOTPView.as_view(), name='otp'),

]
