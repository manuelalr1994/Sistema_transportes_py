from django.shortcuts import render, redirect

# Create your views here.
def HomeNomina(request):
    if request.user.permisos_nomina:
        if request.method == "POST":
            return render(request, 'home/home_nomina.html')
        
        else:
            return render(request, 'home/home_nomina.html')
    else:
        return redirect('users_app:user_error')