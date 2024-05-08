from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from app.home.models import Comunidad, Empresa, User, UserProfile
from .forms import LoginForm, SignUpForm, TokenForm


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



def login_admin_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.user_rol == "lume":
                    login(request, user)
                    return redirect("/admin_lume/index.html")
                else:
                    msg = '¡No tienes permisos para acceder a esta área!'
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
        token_form = TokenForm(request.POST)
        if form.is_valid() and token_form.is_valid():

            email = form.cleaned_data.get("email")
            token = token_form.cleaned_data.get("token")
            
            empresa = Empresa.objects.filter(token=token).first()
            comunidad = Comunidad.objects.filter(token=token).first()

            if empresa:
                user_rol = "company_user"
                
            elif comunidad:
                user_rol = "community_user"

            elif token == "LUME12345678":
                user_rol = "lume"

            else:
                msg = '¡El token proporcionado no es válido!'
                return render(request, "accounts/register.html", {"form": form, "token_form": token_form, "msg": msg, "success": success})

            if User.objects.filter(email=email).exists():
                msg = '¡El correo electrónico ya está en uso!'
            else:
                user = form.save()
                profile = UserProfile.objects.create(user=user, user_rol=user_rol)  # Asignar el valor de user_rol
                password = form.cleaned_data.get("password1")
                user = authenticate(username=email, password=password)
                msg = '¡Usuario creado correctamente!'
                success = True

        else:
            msg = '¡Formulario no válido!'
            success = False
    else:
        form = SignUpForm()
        token_form = TokenForm()

    return render(request, "accounts/register.html", {"form": form, "token_form": token_form, "msg": msg, "success": success})





def logout_view(request):
    
    logout(request)
    return redirect('/login/login/')
