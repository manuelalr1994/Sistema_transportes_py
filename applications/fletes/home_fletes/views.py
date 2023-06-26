from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def HomeFletes(request):
    if request.user.permisos_fletes:
        if request.method == "POST":
            return render(request, 'home/home_fletes.html')
        
        else:
            return render(request, 'home/home_fletes.html')
    return redirect('users_app:user_error')