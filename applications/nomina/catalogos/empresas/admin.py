from django.contrib import admin
from .models import NomEmpresas

# Register your models here.
class EmpresasAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre', 'activo')

admin.site.register(NomEmpresas, EmpresasAdmin)