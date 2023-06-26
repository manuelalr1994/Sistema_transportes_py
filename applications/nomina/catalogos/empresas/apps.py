from django.apps import AppConfig


class EmpresasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.nomina.catalogos.empresas'
    label = 'nom_empresas'

    class Meta:
        app_label = 'NomEmpresas'