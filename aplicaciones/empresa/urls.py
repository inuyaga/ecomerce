from django.contrib import admin
from django.urls import path, include
from aplicaciones.empresa import views
app_name='empresa'
urlpatterns = [
    path('crear_zona/', views.ZonaCreate.as_view(), name='crear_zona'),
    path('zonas/', views.ZonaList.as_view(), name='list_zona'),
    path('zona/actualizar/<int:pk>', views.ZonaUpdate.as_view(), name='zona_edit'),
    path('zona/eliminar/<int:pk>', views.ZonaDelete.as_view(), name='zona_delete'),

    path('sucursales/', views.SucursalList.as_view(), name='list_sucursales'),
    path('sucursales/Ccrear/', views.SucursalCreate.as_view(), name='sucursal_crear'),
    path('sucursales/update/<int:pk>/', views.SucursalUpdate.as_view(), name='sucursal_update'),
    path('sucursales/delete/<int:pk>/', views.SucursalDelete.as_view(), name='sucursal_delete'),

]
