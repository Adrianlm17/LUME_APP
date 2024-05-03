import os
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import TemplateDoesNotExist, loader
from django.urls import reverse
from app.home.forms import UserForm, UserProfileEditForm
from app.home.models import UserProfile
from core import settings





@login_required(login_url="/login/login/")
def home_index(request):

    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/login/")
def pages(request):

    context = {}
    
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))


    # ------------------------ EXCEPTS ------------------------
    except TemplateDoesNotExist:

        html_template = loader.get_template('errors/404.html')
        return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/login/")
def edit_profile(request):
    user_instance = request.user
    profile_instance, created = UserProfile.objects.get_or_create(user=user_instance)
    
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user_instance)
        profile_form = UserProfileEditForm(request.POST, request.FILES, instance=profile_instance)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_instance = profile_form.save(commit=False)
            profile_instance.save()
            return redirect('config')
    
    else:
        user_form = UserForm(instance=user_instance)
        profile_form = UserProfileEditForm(instance=profile_instance)
    
    return render(request, "home/config.html", {"user_form": user_form, "profile_form": profile_form})
