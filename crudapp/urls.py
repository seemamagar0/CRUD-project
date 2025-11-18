from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('students/', StudentListCreate.as_view(), name='student-list-create'),
    path('', views.home, name="home"),
    path('form/', views.form, name='form'),
    path('about/',views.about, name="about"),
    path('add/', views.add, name="add"),
    path('edit/<int:id>/', views.edit, name="edit"),
    # path('delete/<int:id>/', views.delete, name="delete"),
     path('students/<int:id>/update/', StudentUpdate.as_view(), name='student-update'),
    path('students/<int:id>/delete/', StudentDelete.as_view(), name='student-delete'),
]
from django.urls import path
from .views import *

urlpatterns = [
    # API Endpoints
    path('students/', StudentListCreate.as_view(), name='student-list-create'),
    path('students/<int:id>/update/', StudentUpdate.as_view(), name='student-update'),
    path('students/<int:id>/delete/', StudentDelete.as_view(), name='student-delete'),

    # Frontend Pages
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('form/', form, name='form'),
    path('add/', add, name='add'),
    path('edit/<int:id>/', edit, name='edit'),
    path('delete/<int:id>/', delete, name='delete'),
]
