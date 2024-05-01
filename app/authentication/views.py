from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/home/index.html")
            else:
                msg = '¡Credenciales inválidas!'
        else:
            msg = '¡Error al validar el formulario!'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})




def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=email, password=password)

            msg = '¡Usuario creado correctamente!'
            success = True

        else:
            msg = '¡Formulario no valido!'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})



def logout_view(request):
    
    logout(request)
    return redirect('/login/login/')
