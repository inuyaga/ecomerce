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
class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ('dtl_cantidad', 'dtl_codigo')
    def __init__(self, *args, **kwargs):
        super(DetallePedidoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})