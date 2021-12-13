from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import registrationView, logoutView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', registrationView, name='register'),
    path('logout/', logoutView, name='logout'),

    # path('api/token/', TokenObtainPairView.as_view(), name='token obtain pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token refresh'),
]