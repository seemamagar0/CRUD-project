from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('students/', StudentListCreate.as_view(), name='student-list-create'),
    path('edit/<int:id>/', views.edit, name="edit"),
    # path('delete/<int:id>/', views.delete, name="delete"),
     path('students/<int:id>/update/', StudentUpdate.as_view(), name='student-update'),
    path('students/<int:id>/delete/', StudentDelete.as_view(), name='student-delete'),

    
]
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # API Endpoints
    path('api/register/', views.UserRegistrationAPIView.as_view(), name='api_register'),
    path('students/', StudentListCreate.as_view(), name='student-list-create'),
    path('students/<int:id>/update/', StudentUpdate.as_view(), name='student-update'),
    path('students/<int:id>/delete/', StudentDelete.as_view(), name='student-delete'),

    # Frontend Pages
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('form/', form, name='form'),
    path('services/',views.services, name='services'),
    path('edit/<int:id>/', edit, name='edit'),
    path('delete/<int:id>/', delete, name='delete'),

    path("register/",register,name='register'),
    path("login/",log_in,name="log_in"),
    path("logout/",log_out,name="log_out"),

    path('api/login/', UserLoginAPIView.as_view(), name='api_login'),

      # JWT login
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]
