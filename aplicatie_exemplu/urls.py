"""
URL configuration for magazin_cosmetice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views. index, name="index"),
    path( 'info', views. info, name="info"),
    path( 'exemplu_template', views.exemplu_template, name="exemplu_template"),
    path( 'exemplu_template2', views.exemplu_template2, name="exemplu_template2"),
    path('log', views.log_view, name='log'),
    path('istoric', views.istoric, name='istoric'),
    path('despre', views.despre, name='despre'),
    re_path(r'^accesare(?P<id>\d+)$', views.detalii_accesare, name='detalii_accesare'),#ia cifrele de dupa /accesare
    path('produs', views.afisare_produse, name="afisare_produse"),
    
]
