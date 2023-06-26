from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

app_name = "users_app"

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('panel/', PanelPage.as_view(), name='user_panel'),
    path('login/', LoginUser.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('update/', UpdatePasswordView.as_view(), name='user_update'),
    path('inicio/', InicioUsuarios.as_view(), name='user_list'),
    path('error/', SinAccesoPage.as_view(), name='user_error'),
    path('consulta/<pk>/', DetailUsuarios.as_view(), name='user_consulta'),
]
