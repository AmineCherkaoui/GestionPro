from django.urls import path
from . import views


urlpatterns=[
    path("",views.services_list,name="services-list"),
    path("new/",views.create_service,name="create-service"),
    path("edit/<int:service_id>/",views.edit_service,name="edit-service"),
    path("delete/<int:service_id>/",views.delete_service,name="delete-service"),
]