from django.urls import path
from . import views


urlpatterns = [
    path("",views.suppliers_list,name="suppliers-list"),
    path('new/', views.create_supplier, name='create-supplier'),
    path("edit/<int:supplier_id>", views.edit_supplier, name="edit-supplier"),
    path("delete/<int:supplier_id>", views.delete_supplier, name="delete-supplier")
]