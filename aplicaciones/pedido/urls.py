from django.contrib import admin
from django.urls import path, include
from aplicaciones.pedido import views

app_name='pedido'
urlpatterns = [
    path('ProductoList/',views.ProductoLista.as_view(),name="ProductoLista"),
    # path('ProductoList/',views.ProductoLista.as_view(),name="ProductoLista"),
]
