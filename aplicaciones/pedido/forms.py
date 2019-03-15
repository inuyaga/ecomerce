from django import forms
from aplicaciones.pedido.models import *

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('__all__')
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})