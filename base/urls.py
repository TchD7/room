from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logoutUser, name = 'logout'),
    path('login/', views.loginPage, name = 'login'),
    path('register/', views.registerPage, name = 'register'),
    path('', views.home, name = 'home'),
    path('room/<str:pk>', views.room, name = 'room'),
    path('create-room/', views.createRoom, name = 'create-room'),
    path('update-room/<str:pk>', views.updateroom, name = 'update-room'),
    path('delete/<str:pk>', views.deleteRoom, name = 'delete'),
] 