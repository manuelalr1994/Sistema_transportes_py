from django.contrib import admin
from .models import CompaniasFleteras

# Register your models here.
class CompaniasFleterasAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre', 'activo')

admin.site.register(CompaniasFleteras, CompaniasFleterasAdmin)