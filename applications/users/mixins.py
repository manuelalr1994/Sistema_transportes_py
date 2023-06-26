from django import dispatch
from django.shortcuts import redirect
from django.urls import reverse_lazy

############################################################ LOGIN MIXIN ################################################################
class LoginAndSuperUserMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser: # o is_staff
                return super().dispatch(request, *args, **kwargs)
        return redirect('users_app:user_error')

class LoginAndStaffMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff: # o is_staff
                return super().dispatch(request, *args, **kwargs)
        return redirect('users_app:user_error')

class LoginAndActiveMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_active:
                return super().dispatch(request, *args, **kwargs)
        return redirect('users_app:user_login')

############################################################ PERMISOS MIXIN ################################################################
class PermisoFacturacion(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.permisos_facturacion:
                return super().dispatch(request, *args, **kwargs)
        return redirect('users_app:user_error')

class PermisoFletes(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.permisos_fletes:
                return super().dispatch(request, *args, **kwargs)
        return redirect('users_app:user_error')

class PermisoFlotilla(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.permisos_flotilla:
                return super().dispatch(request, *args, **kwargs)
        return redirect('users_app:user_error')

class PermisoNomina(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.permisos_nomina:
                return super().dispatch(request, *args, **kwargs)
        return redirect('users_app:user_error')






"""class ValidarPermisosRequeridosMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required,str):
            return (self.permission_required)
        else:
            return self.permission_required

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('fletes:home')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        return redirect(self.get_url_redirect())
    """