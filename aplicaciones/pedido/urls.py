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
    path('Carrito/',views.CarritoLista.as_view(),name="carrito"),

    path('delete_datailproducto/<int:pk>/',views.CarritoDelete.as_view(),name="delete_datailproducto"),
    path('descarga_pedido/<int:pk>/',views.DowloadExcelPedido.as_view(),name="descarga_pedido"),
    path('detalle_pedido/<int:pk>/',views.DetallePedidolit.as_view(),name="detalle_pedido"),

    path('AutorizaPedido/<int:pk>/',views.AutorizarPedido.as_view(),name="auto_pedido"),
    path('RechazaraPedido/<int:pk>/',views.RechazarPedido.as_view(),name="rechaza_pedido"),
    path('pedido_update/<int:pk>/',views.PedidoUpdate.as_view(),name="pedido_update"),

    path('informacion_pedido/<int:pk>/',views.PedidoDetalleList.as_view(),name="pedido_info"),
]
