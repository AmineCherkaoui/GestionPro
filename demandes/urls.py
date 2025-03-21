from . import views
from django.urls import path



urlpatterns = [
    # Demande de caution
    path("caution", views.demande_cautions_list, name="demandes-caution-list"),
    path("caution/new/",views.create_demande_caution,name="create-demande-caution"),
    path("caution/<int:demande_caution_id>/edit",views.edit_demande_caution,name="edit-demande-caution"),
    path("caution/<int:demande_caution_id>/delete",views.delete_demande_caution,name="delete-demande-caution"),
    path("caution/<int:demande_caution_id>/pdf",views.demande_caution_pdf,name="demande-caution-pdf"),
    # Demade De virement
    path("virement",views.demande_virement_list,name="demande-virement-list"),
    path("virement/new/",views.create_demande_virement,name="create-demande-virement"),
    path("virement/<int:demande_virement_id>/edit",views.edit_demande_virement,name="edit-demande-virement"),
    path("virement/<int:demande_virement_id>/delete",views.delete_demande_virement,name="delete-demande-virement"),
    path("virement/<int:demande_virement_id>/pdf",views.demande_virement_pdf,name="demande-virement-pdf"),
]
