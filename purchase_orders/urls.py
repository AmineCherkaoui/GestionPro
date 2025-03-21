from django.urls import path
from . import views


urlpatterns = [
    path("out/",views.purchase_orders_list,name="purchase-orders-list"),
    path("out/new/",views.create_purchase_order,name="create-purchase-order"),
    path("out/<int:purchase_order_id>/delete",views.delete_purchase_order,name="delete-purchase-order"),
    path("out/<int:purchase_order_id>/details",views.purchase_order_details,name="purchase-order-detail"),
    path("out/<int:purchase_order_id>/pdf",views.purchase_order_pdf,name="purchase-order-pdf"),
    path("out/<int:purchase_order_id>/add-product",views.purchase_order_add_product,name="purchase-order-add-product"),
    path("out/<int:purchase_order_id>/product/<int:product_id>", views.purchase_order_delete_product, name="purchase-order-delete-product"),

    path("out/<int:purchase_order_id>/add-service",views.purchase_order_add_service,name="purchase-order-add-service"),
    path("out/<int:purchase_order_id>/service/<int:service_id>", views.purchase_order_delete_service, name="purchase-order-delete-service"),

]