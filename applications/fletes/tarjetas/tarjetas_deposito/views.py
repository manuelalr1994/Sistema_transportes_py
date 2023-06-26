from django.shortcuts import render, redirect

# Create your views here.

def listaTarjetas(request):
    if request.user.permisos_fletes:
        html_template = "fletes/tarjetas/tarjetas.html"
        return render(request, html_template)
    else:
        return redirect('users_app:user_error')