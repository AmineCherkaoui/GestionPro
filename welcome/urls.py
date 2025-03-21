from django.urls import path
from . import views


urlpatterns = [
    path("",views.welcome,name="welcome"),
    path('create-user/', views.create_user, name='welcome-create-user'),
    path('create-settings/',views.create_settings, name='welcome-create-settings'),
]