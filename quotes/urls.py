from django.urls import path
from . import views
urlpatterns = [
    path('out/', views.quotes_list, name="quotes-list"),
    path("out/new", views.create_quote, name="create-quote"),
    path("out/<int:quote_id>/", views.quote_details, name="quote-detail"),
    path("out/<int:quote_id>/delete", views.delete_quote, name="delete-quote"),
    path("out/<int:quote_id>/pdf",views.quote_pdf,name="quote-pdf"),
    path("out/<int:quote_id>/add-product/", views.quote_add_product, name="quote-add-product"),
    path("out/<int:quote_id>/details/add-service/", views.quote_add_service, name="quote-add-service"),
    path("out/<int:quote_id>/product/<int:product_id>", views.quote_delete_product, name="quote-delete-product"),
    path("out/<int:quote_id>/service/<int:service_id>", views.quote_delete_service, name="quote-delete-service"),
    path('out/<int:quote_id>/convert-to-invoice/', views.convert_quote_to_invoice, name='quote-to-invoice'),

]