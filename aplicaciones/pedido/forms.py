from django import forms
from aplicaciones.pedido.models import *

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('__all__')
        widgets = {
        'prod_descripcion': forms.Textarea(),
        }
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('ped_pdffac', 'ped_xmlfac')
        # widgets = {
        # 'prod_descripcion': forms.Textarea(),
        # }
    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].required = True


class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ('dtl_cantidad', 'dtl_codigo')
    def __init__(self, *args, **kwargs):
        super(DetallePedidoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
class DetallePedidoFormEdit(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ('dtl_id_pedido','dtl_cantidad')
    def __init__(self, *args, **kwargs):
        super(DetallePedidoFormEdit, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ConfForm(forms.ModelForm):
    class Meta:
        model = Configuracion_pedido
        fields = ('__all__')
        widgets = {
        'conf_fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
        'conf_fecha_fin' : forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(ConfForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ConfFormEdit(forms.ModelForm):
    class Meta:
        model = Configuracion_pedido
        fields = ('__all__')
    def __init__(self, *args, **kwargs):
        super(ConfFormEdit, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
