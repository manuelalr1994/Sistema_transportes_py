from django.contrib import admin
from .models import NomPuestos

# Register your models here.
class PuestosAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre', 'activo')

admin.site.register(NomPuestos, PuestosAdmin)