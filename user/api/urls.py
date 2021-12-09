from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import registrationView, logoutView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', registrationView, name='register'),
    path('logout/', logoutView, name='logout')
]