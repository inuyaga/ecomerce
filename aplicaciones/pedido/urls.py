from django.contrib import admin
from django.urls import path, include
from aplicaciones.pedido import views

app_name='pedido'
urlpatterns = [
    path('ProductoList/',views.ProductoLista.as_view(),name="ProductoLista"),
    path('Producto/crear/',views.PrductoCreate.as_view(),name="crear_producto"),
    path('Producto/update/<int:pk>',views.ProductoUpdate.as_view(),name="changue_producto"),
    path('Producto/delete/<int:pk>',views.ProductoDelete.as_view(),name="delete_producto"),
    path('pedido/list/',views.PedidoList.as_view(),name="listar_pedido"),
]
