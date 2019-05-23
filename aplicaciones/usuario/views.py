from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.usuario.forms import UserForm, UserFormEdit, UserFormEditPermNormal
from aplicaciones.usuario.models import User
from django.contrib.auth.admin import UserAdmin
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm, PasswordResetConfirmView
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.db.models import Q

from django.core.mail import send_mail, EmailMultiAlternatives
# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


class CreateUser(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to' 
    model = UserAdmin
    form_class = UserForm
    template_name = 'admin/crear_usuarios.html'
    success_url = reverse_lazy('usuarios:list_user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context
    def form_valid(self, form):
        
        # message = render_to_string('email_template.html', {'user': form.instance.username, 'pass': form.instance.password, 'url': url})

        # email = send_mail('Creacion de usuario', message, 'soporte@computel.com.mx', [form.instance.email])
        # email.send()
        current_site = str(get_current_site(self.request))
        url="http://{}".format(current_site)

        subject, from_email, to = 'Creacion de usuario', 'soporte@computel.com.mx', form.cleaned_data['email']
        text_content = 'Creacion de usuario de'
        html_content = render_to_string('email_template.html', 
                                        {
                                        'user': form.cleaned_data['username'], 
                                        'pass': form.cleaned_data['password1'], 
                                        'url': url,
                                        'sitio': current_site
                                        })
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        self.object = form.save()
        return super().form_valid(form)

    


    @method_decorator(permission_required('usuario.add_user',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(CreateUser, self).dispatch(*args, **kwargs)

class UsuarioList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = User
    template_name = 'admin/list_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

    def get_queryset(self):
        queryset = super(UsuarioList, self).get_queryset()
        busqueda=self.request.GET.get('buscar')
        if busqueda != None:
            queryset=queryset.filter(Q(username__icontains=busqueda) | Q(first_name__icontains=busqueda))
        return queryset

    @method_decorator(permission_required('usuario.view_user',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(UsuarioList, self).dispatch(*args, **kwargs)

class UsuarioUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = User
    form_class = UserFormEdit
    template_name = 'admin/crear_usuarios.html'
    success_url = reverse_lazy('usuarios:list_user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context



    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                pass
            else:
                return redirect('/')
        return super().dispatch(*args, **kwargs)



class UsuarioUpdatePermNormal(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = User
    form_class = UserFormEditPermNormal
    template_name = 'admin/crear_usuarios.html'
    success_url = reverse_lazy('usuarios:list_user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

    @method_decorator(permission_required('usuario.change_user',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(UsuarioUpdatePermNormal, self).dispatch(*args, **kwargs)

class ChaguePasswordUser(LoginRequiredMixin, PasswordChangeView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = User
    form_class = PasswordChangeForm
    template_name = 'changuepassword.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

class PasswordUpdate(PasswordChangeView):
    model=User
    template_name='changuepassword.html'
    form_class=AdminPasswordChangeForm
    success_url='/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context
    def form_valid(self, form):
        self.object = form.save(commit=False)
        id_user=self.kwargs.get('pk')
        u = User.objects.get(id=id_user)
        u.set_password(self.request.POST.get('password1'))
        u.save()
        url=reverse_lazy('usuarios:list_user')
        return redirect(url)



