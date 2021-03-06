
from django.contrib import admin
from django.urls import path, include
from aplicaciones.empresa.views import inicio
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('emp/', include('aplicaciones.empresa.urls'), name='ec_empresa'),
    path('pedido/', include('aplicaciones.pedido.urls'), name='ec_pedido'),
    path('user/', include('aplicaciones.usuario.urls'), name='ec_usuario'),
    path('', inicio.as_view(), name='index'),
    path('login/',LoginView.as_view(template_name='login_ecomer.html'), name='login'),
    path('salir/', LogoutView.as_view(template_name='logout.html'), name="salir"),
    path('requiere_permisos/', TemplateView.as_view(template_name='error_permisos.html'), name="requiere_permisos"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
