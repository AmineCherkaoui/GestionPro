"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("",RedirectView.as_view(url="dashboard")),
    path('dashboard/', include('dashboard.urls')),
    path("login/",auth_views.LoginView.as_view(),name="login"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path('clients/', include("clients.urls")),
    path("suppliers/",include("suppliers.urls")),
    path("products/",include("products.urls")),
    path("services/",include("services.urls")),
    path("invoices/",include("invoices.urls")),
    path("quotes/",include("quotes.urls")),
    path("purchase-orders/",include("purchase_orders.urls")),
    path("demandes/", include("demandes.urls")),
    path("welcome/",include("welcome.urls")),
    path("admin/settings/",include("settings.urls")),
    path("admin/users/",include("users.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)