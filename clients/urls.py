from django.urls import path
from . import views

urlpatterns = [
    path('', views.clients_list,name="clients-list"),
    path('new/', views.create_client, name='create-client'),
    path("edit/<int:client_id>",views.edit_client,name="edit-client"),
    path("delete/<int:client_id>",views.delete_client,name="delete-client")
]