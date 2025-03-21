from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_list,name="products-list"),
    path('new/', views.create_product, name='create-product'),
    path("edit/<int:product_id>",views.edit_product,name="edit-product"),
    path("delete/<int:product_id>",views.delete_product,name="delete-product")
]