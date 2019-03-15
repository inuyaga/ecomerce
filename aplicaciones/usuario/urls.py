
from django.urls import path, include
from aplicaciones.usuario import views

app_name='usuarios'
urlpatterns = [
    path('crear_usuario/',views.CreateUser.as_view(),name='crear_user' ),
    path('usuario/list/',views.UsuarioList.as_view(),name='list_user' ),
    path('usuario/update/<int:pk>/',views.UsuarioUpdate.as_view(),name='user_update' ),
]
