from django import forms
from django.contrib.auth.forms import UserCreationForm
from aplicaciones.usuario.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
class UserFormEdit(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['password', 'last_login', 'date_joined', 'is_staff']

    def __init__(self, *args, **kwargs):
        super(UserFormEdit, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs['readonly'] = True
        # self.fields['is_superuser'].widget.attrs.update({'class': 'form-check-input'})
        # self.fields['is_staff'].widget.attrs.update({'class': 'form-check-input'})
        # self.fields['is_active'].widget.attrs.update({'class': 'form-check-input'})
