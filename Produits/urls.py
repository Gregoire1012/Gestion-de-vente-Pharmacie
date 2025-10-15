from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.urls import path, include  # <-- ajouter include ici
from django.contrib import admin

urlpatterns = [
    path('',Acc,name='acc'),
    path('home', Affichage.as_view(), name='home'),
    path('ajout/', ajout_donnees, name='ajout'),
    # Si tu as une fonction product_list dans views.py, sinon supprime la ligne
    # path('', product_list, name='product_list'),
    path('detail/<int:pk>/', product_detail, name='product_detail'),
    path('edit/<int:pk>/', edit_product, name='edit_product'),  # ✅ nouvelle route
    path('delete/<int:pk>/', delete_product, name="delete_product"),  # ✅ Ajout suppression
    path("recherche/", recherche, name="recherche"),

    path('ajoutvente/<int:id>/', views.ajoutvente, name='ajoutvente'),
    path('ventes/', views.liste_ventes, name='liste_ventes'),
    path('enregistrement-recu/<int:id>/', Saverecu, name='saverecu'),
    path('facture/<int:vente_id>/', views.facture, name='facture'),
    path('dashboard/', views.dashboard, name='dashboard'),

   






] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
