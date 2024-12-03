"""
URL configuration for ecommers project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import os

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("", include("main.urls"), name="main"),
    path("products/", include("products.urls"), name="products"),
    path("payments/", include("payments.urls"), name="payments"),
    path("accounts/", include("accounts.urls"), name="accounts"),
    
    # path("orders/", include("orders.urls"), name="orders"),
    
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Se le da esto en la carpeta principal del proyecto y no en la aplicaciones

# Servir media en desarrollo y producción
if settings.DEBUG or os.environ.get('RENDER'): 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Se le da esto en la carpeta principal del proyecto y no en la aplicaciones