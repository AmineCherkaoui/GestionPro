from django.urls import path
from . import views
urlpatterns = [
    path('out/', views.invoices_list, name="invoices-list"),
    path("out/new", views.create_invoice, name="create-invoice"),
    path("out/<int:invoice_id>/pdf",views.invoice_pdf,name="invoice-pdf"),
    path("out/<int:invoice_id>/", views.invoice_details, name="invoice-detail"),
    path("out/<int:invoice_id>/add-product/", views.invoice_add_product, name="invoice-add-product"),
    path("out/<int:invoice_id>/product/<int:product_id>", views.invoice_delete_product, name="invoice-delete-product"),
    path("out/<int:invoice_id>/service/<int:service_id>", views.invoice_delete_service, name="invoice-delete-service"),
    path("out/<int:invoice_id>/details/add-service/", views.invoice_add_service, name="invoice-add-service"),
    path("out/<int:invoice_id>/delete", views.delete_invoice, name="delete-invoice"),

]