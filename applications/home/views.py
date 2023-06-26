from django.urls import reverse_lazy
from django.views.generic import TemplateView
from applications.users.mixins import LoginAndActiveMixin

from django.shortcuts import render, redirect


class UbicacionesHome(LoginAndActiveMixin, TemplateView):
    template_name = "home/ubicaciones.html"
    login_url = reverse_lazy('users_app:user_login')

class ModulosHome(LoginAndActiveMixin, TemplateView):
    template_name = "home/modulos.html"
    login_url = reverse_lazy('users_app:user_login')

    # SET COOKIE
    # def get(self, request):
    #     ubicacion_usuario = request.GET.get('ubicacion_usuario')
    #     response = render(request, self.template_name)
    #     response.set_cookie('ubicacion_usuario', ubicacion_usuario, samesite='None', secure=True)
    #     return response