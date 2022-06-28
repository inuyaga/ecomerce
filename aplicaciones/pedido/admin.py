from django.contrib import admin
from aplicaciones.pedido.models import ConfigRestriccion


class ConfigRestriccionAdmin(admin.ModelAdmin):
    list_display = [
        'conf_r_fecha_inicio',
        'conf_r_fecha_fin',
        'conf_r_tipo_pedido',
    ]


admin.site.register(ConfigRestriccion, ConfigRestriccionAdmin)