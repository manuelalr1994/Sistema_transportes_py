from multiprocessing import context
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView, View, ListView, DetailView
from django.views.generic.edit import FormView
from .mixins import LoginAndSuperUserMixin, LoginAndStaffMixin, LoginAndActiveMixin

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm
from .models import User

class UserRegisterView(LoginAndSuperUserMixin, FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users_app:user_login')
    login_url = reverse_lazy('users_app:user_login')

    def form_valid(self, form):

        user = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            # permisos_ubicaciones=form.cleaned_data['permisos_ubicaciones'],
        )

        # user.permisos_ubicaciones.set(form.cleaned_data['permisos_ubicaciones'])
        
        return super(UserRegisterView, self).form_valid(form)


class InicioUsuarios(LoginAndStaffMixin, ListView):
    model = User
    template_name = 'users/list_user.html'

    def get_context_data(self, **kwargs):
        context = {}
        user_buscado = self.request.GET.get('user_buscado')
        if user_buscado is not None:
            context['lista_user'] = self.model.objects.filter(nombre__icontains=user_buscado)
        else:
            context['lista_user'] = self.model.objects.all()

        for user in context['lista_user']:
            user.id = str(user.id)

        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class DetailUsuarios(LoginAndStaffMixin, DetailView):
    model = User
    template_name = 'users/consulta_user.html'
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        context = super(DetailUsuarios, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home:home_ubicaciones')

    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):

    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:user_login'
            )
        )


class UpdatePasswordView(LoginAndActiveMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user_login')
    login_url = reverse_lazy('users_app:user_login')

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()

            logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)


############################################ PANEL #############################################################


class PanelPage(LoginAndActiveMixin, TemplateView):
    template_name = "users/panel.html"
    login_url = reverse_lazy('users_app:user_login')


############################################ ERROR MIXIN #######################################################

class SinAccesoPage(LoginAndActiveMixin, TemplateView):
    template_name = "users/sin_acceso.html"
    login_url = reverse_lazy('users_app:user_login')