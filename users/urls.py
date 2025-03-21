from django.urls import path
from . import views


urlpatterns=[
    path("",views.users_list,name="users-list"),
    path("new/",views.create_user,name="create-user"),
    path("<int:user_id>/edit/",views.edit_user,name="edit-user"),
    path("<int:user_id>/delete/",views.delete_user,name="delete-user"),
    path("<int:user_id>/status/",views.toggle_active_user,name="change-user-status"),
]