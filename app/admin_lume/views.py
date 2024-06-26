import secrets
from geopy.geocoders import Nominatim
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from app.authentication.forms import SignUpForm
from app.home.forms import UpdateProfileForm
from app.home.models import Comunidad, Empresa, Trabajador, User, Vivienda
from django.shortcuts import get_object_or_404, render
from django.template import TemplateDoesNotExist, loader
from django.urls import reverse
from app.admin_lume.forms import CrearCompanyForm, CrearComunidadForm, CrearTrabajadorForm, CrearUserProfileForm, CrearViviendaForm



# ---------------------------------------------------------- INDEX ---------------------------------------------------------- 
@login_required(login_url="/login/login_admin/")
def admin_index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('admin_lume/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/login_admin/")
def pages(request):

    context = {}
    
    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        
        context['segment'] = load_template
        html_template = loader.get_template('admin_lume/' + load_template)
        return HttpResponse(html_template.render(context, request))

    # ------------------------ EXCEPTS ------------------------
    except TemplateDoesNotExist:
        html_template = loader.get_template('errors/404.html')
        return HttpResponse(html_template.render(context, request))





# ---------------------------------------------------------- USER ---------------------------------------------------------- 
@login_required(login_url="/login/login_admin/")
def user_list(request):
    users = User.objects.all()

    return render(request, 'admin_lume/users.html', {'segment': 'ver_usuario', 'users': users})


@login_required(login_url="/login/login_admin/")
def create_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        form_profile = CrearUserProfileForm(request.POST)
        if form.is_valid() and form_profile.is_valid():
            email = form.cleaned_data.get("email")
            
            if User.objects.filter(email=email).exists():
                msg = '¡El correo electrónico ya está en uso!'

            else:
                user = form.save()
                profile = form_profile.save(commit=False) 
                profile.user = user
                profile.save()
                password = form.cleaned_data.get("password1")
                user = authenticate(username=email, password=password)
                success = True

        else:
            msg = '¡Formulario no válido!'

    else:
        form = SignUpForm()
        form_profile = CrearUserProfileForm()

    return render(request, "admin_lume/create_user.html", {'segment': 'create_user', "form": form, "form_profile" : form_profile, "msg": msg, "success": success})


@login_required(login_url="/login/login_admin/")
def edit_user(request, user_id):
    msg = None
    success = False
    user = get_object_or_404(User, id=user_id)
    profile_instance = user.userprofile

    if request.method == "POST":
        user_form = UpdateProfileForm(request.POST, instance=user)
        profile_form = CrearUserProfileForm(request.POST, instance=profile_instance)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            success = True

        else:
            msg = '¡Formulario no válido!'

    else:
        user_form = UpdateProfileForm(instance=user)
        profile_form = CrearUserProfileForm(instance=profile_instance)

    return render(request, "admin_lume/edit_user.html", {'segment': 'ver_usuario', "user_form": user_form, "profile_form" : profile_form, "msg": msg, "success": success})


@login_required(login_url="/login/login_admin/")
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
    
    users = User.objects.all()

    return render(request, 'admin_lume/users.html', {'segment': 'ver_usuario', 'users': users})





# ---------------------------------------------------------- COMMUNITYS ---------------------------------------------------------- 
@login_required(login_url="/login/login_admin/")
def community_list(request):
    communitys = Comunidad.objects.all()

    return render(request, 'admin_lume/communitys.html', {'segment': 'ver_comunidad', 'communitys': communitys})


def create_community(request):
    msg = None
    success = False

    if request.method == 'POST':
        form = CrearComunidadForm(request.POST)

        if form.is_valid():
            comunidad = form.save(commit=False)
            comunidad.token = secrets.token_urlsafe(16)
            direccion = f"{comunidad.dirrecion}, {comunidad.municipio}, {comunidad.provincia}, {comunidad.pais}"
            geolocalizador = Nominatim(user_agent="my_geocoder")
            try:
                ubicacion = geolocalizador.geocode(direccion)
                
                if ubicacion:
                    comunidad.lat = ubicacion.latitude
                    comunidad.lng = ubicacion.longitude
                    
            except:
                ubicacion = direccion

            

            comunidad.save()
            success = True
        
        else:
            msg = '¡Formulario no válido!'   
    
    else:
        form = CrearComunidadForm()

    return render(request, 'admin_lume/create_community.html', {'segment': 'crear_comunidad', "form": form, "msg": msg, "success": success})


def edit_community(request, communitys_id):
    msg = None
    success = False
    communitys = get_object_or_404(Comunidad, id=communitys_id)

    if request.method == "POST":
        communitys_form = CrearComunidadForm(request.POST, instance=communitys)
        
        if communitys_form.is_valid():
            direccion = f"{communitys_form.cleaned_data['dirrecion']}, {communitys_form.cleaned_data['municipio']}, {communitys_form.cleaned_data['provincia']}, {communitys_form.cleaned_data['pais']}"
            geolocalizador = Nominatim(user_agent="my_geocoder")
            ubicacion = geolocalizador.geocode(direccion)

            if ubicacion:
                communitys_form.instance.lat = ubicacion.latitude
                communitys_form.instance.lng = ubicacion.longitude

            communitys_form.save()
            success = True

        else:
            msg = '¡Formulario no válido!'

    else:
        communitys_form = CrearComunidadForm(instance=communitys)

    return render(request, "admin_lume/edit_community.html", {'segment': 'ver_comunidad', "communitys_form": communitys_form, "msg": msg, "success": success})


@login_required(login_url="/login/login_admin/")
def delete_community(request, communitys_id):
    community = get_object_or_404(Comunidad, id=communitys_id)

    if request.method == 'POST':
        community.delete()
    
    communitys = Comunidad.objects.all()
    return render(request, 'admin_lume/communitys.html', {'segment': 'ver_comunidad', 'communitys': communitys})






# ---------------------------------------------------------- COMPANY ---------------------------------------------------------- 
@login_required(login_url="/login/login_admin/")
def company_list(request):
    companys = Empresa.objects.all()
    return render(request, 'admin_lume/companys.html', {'segment': 'ver_empresa', 'companys': companys})


def create_company(request):
    msg = None
    success = False

    if request.method == 'POST':
        company = CrearCompanyForm(request.POST)

        if company.is_valid():
            comunidad = company.save(commit=False)
            comunidad.token = secrets.token_urlsafe(16)
            direccion = f"{comunidad.direccion}, {comunidad.municipio}, {comunidad.provincia}, {comunidad.pais}"
            geolocalizador = Nominatim(user_agent="my_geocoder")
            ubicacion = geolocalizador.geocode(direccion)

            if ubicacion:
                comunidad.lat = ubicacion.latitude
                comunidad.lng = ubicacion.longitude

            comunidad.save()
            success = True
        
        else:
            msg = '¡Formulario no válido!'   
    
    else:
        company = CrearCompanyForm()

    return render(request, 'admin_lume/create_company.html', {'segment': 'crear_empresa', "company": company, "msg": msg, "success": success})


def edit_company(request, companys_id):
    msg = None
    success = False
    companys = get_object_or_404(Empresa, id=companys_id)

    if request.method == "POST":
        companys_form = CrearCompanyForm(request.POST, instance=companys)
        
        if companys_form.is_valid():
            direccion = f"{companys_form.cleaned_data['direccion']}, {companys_form.cleaned_data['municipio']}, {companys_form.cleaned_data['provincia']}, {companys_form.cleaned_data['pais']}"
            geolocalizador = Nominatim(user_agent="my_geocoder")
            ubicacion = geolocalizador.geocode(direccion)

            if ubicacion:
                companys_form.instance.lat = ubicacion.latitude
                companys_form.instance.lng = ubicacion.longitude

            companys_form.save()
            success = True

        else:
            msg = '¡Formulario no válido!'

    else:
        companys_form = CrearCompanyForm(instance=companys)

    return render(request, "admin_lume/edit_company.html", {'segment': 'ver_comunidad', "companys_form": companys_form, "msg": msg, "success": success})


@login_required(login_url="/login/login_admin/")
def delete_company(request, companys_id):
    company = get_object_or_404(Empresa, id=companys_id)

    if request.method == 'POST':
        company.delete()
    
    companys = Empresa.objects.all()
    return render(request, 'admin_lume/companys.html', {'segment': 'ver_comunidad', 'companys': companys})





# ---------------------------------------------------------- LIVING PLACE ---------------------------------------------------------- 
@login_required(login_url="/login/login_admin/")
def vivienda_list(request):
    viviendas = Vivienda.objects.all()
    return render(request, 'admin_lume/viviendas.html', {'segment': 'ver_vivienda', 'viviendas': viviendas})


@login_required(login_url="/login/login_admin/")
def crear_vivienda(request):
    msg = None
    success = False

    if request.method == 'POST':
        living_place = CrearViviendaForm(request.POST)
        
        if living_place.is_valid():
            living_place.save()
            success = True

        else:
            msg = '¡Formulario no válido!' 
            
    else:
        living_place = CrearViviendaForm()

    return render(request, 'admin_lume/create_viviendas.html', {'segment': 'asignar_vivienda', 'living_place': living_place, "msg": msg, "success": success})


@login_required(login_url="/login/login_admin/")
def edit_vivienda(request, viviendas_id):
    msg = None
    success = False
    viviendas = get_object_or_404(Vivienda, id=viviendas_id)

    if request.method == "POST":
        viviendas_form = CrearViviendaForm(request.POST, instance=viviendas)
        
        if viviendas_form.is_valid():
            viviendas_form.save()
            success = True

        else:
            msg = '¡Formulario no válido!'
    else:
        viviendas_form = CrearViviendaForm(instance=viviendas)

    return render(request, "admin_lume/edit_vivienda.html", {'segment': 'ver_vivienda', "viviendas_form": viviendas_form, "msg": msg, "success": success})


@login_required(login_url="/login/login_admin/")
def delete_vivienda(request, viviendas_id):
    vivienda = get_object_or_404(Vivienda, id=viviendas_id)

    if request.method == 'POST':
        vivienda.delete()
    
    viviendas = Vivienda.objects.all()
    return render(request, 'admin_lume/viviendas.html', {'segment': 'ver_vivienda', 'viviendas': viviendas})





# ---------------------------------------------------------- WORKER ---------------------------------------------------------- 
@login_required(login_url="/login/login_admin/")
def trabajador_list(request):
    trabajadors = Trabajador.objects.all()
    return render(request, 'admin_lume/trabajadores.html', {'segment': 'ver_trabajador', 'trabajadors': trabajadors})


@login_required(login_url="/login/login_admin/")
def crear_trabajador(request):
    msg = None
    success = False

    if request.method == 'POST':
        worker = CrearTrabajadorForm(request.POST)
        
        if worker.is_valid():
            worker.save()
            success = True

        else:
            msg = '¡Formulario no válido!' 
            
    else:
        worker = CrearTrabajadorForm()

    return render(request, 'admin_lume/create_worker.html', {'segment': 'asignar_trabajador', 'worker': worker, "msg": msg, "success": success})


@login_required(login_url="/login/login_admin/")
def edit_trabajador(request, trabajadors_id):
    msg = None
    success = False
    trabajadors = get_object_or_404(Trabajador, id=trabajadors_id)

    if request.method == "POST":
        trabajadors_form = CrearTrabajadorForm(request.POST, instance=trabajadors)
        
        if trabajadors_form.is_valid():
            trabajadors_form.save()
            success = True

        else:
            msg = '¡Formulario no válido!'

    else:
        trabajadors_form = CrearTrabajadorForm(instance=trabajadors)

    return render(request, "admin_lume/edit_trabajador.html", {'segment': 'ver_trabajador', "trabajadors_form": trabajadors_form, "msg": msg, "success": success})


@login_required(login_url="/login/login_admin/")
def delete_trabajador(request, trabajadors_id):
    trabajador = get_object_or_404(Trabajador, id=trabajadors_id)

    if request.method == 'POST':
        trabajador.delete()
    
    trabajadors = trabajador.objects.all()
    return render(request, 'admin_lume/trabajadores.html', {'segment': 'ver_trabajador', 'trabajadors': trabajadors})
