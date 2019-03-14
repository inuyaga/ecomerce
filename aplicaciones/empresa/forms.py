from django import forms
from aplicaciones.empresa.models import Sucursal, Zona
class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ('__all__')
    def __init__(self, *args, **kwargs):
        super(ZonaForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ('__all__')
    def __init__(self, *args, **kwargs):
        super(SucursalForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})