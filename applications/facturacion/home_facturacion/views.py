from django.shortcuts import render, redirect

# Create your views here.
def HomeFacturacion(request):
    if request.user.permisos_facturacion:
        if request.method == "POST":
            return render(request, 'home/home_facturacion.html')
        
        else:
            return render(request, 'home/home_facturacion.html')
    else:
        return redirect('users_app:user_error')