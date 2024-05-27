from django.conf import settings
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.http import HttpResponse
from django.template import TemplateDoesNotExist, loader
from django.shortcuts import redirect
from django.utils import translation





def visits_index(request):
    context = {'segment': 'index'}
    return render(request, 'visits/index.html', context)


def cambiar_idioma(request, idioma):
    translation.activate(idioma)
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, idioma)
    return response


def pages(request):
    
    context = {}

    try:
        load_template = request.path.split('/')[-1]

        html_template = loader.get_template('visits/' + load_template)
        return HttpResponse(html_template.render(context, request))
    
    except TemplateDoesNotExist:
        html_template = loader.get_template('errors/404.html')
        return HttpResponse(html_template.render(context, request))
    
    # except:
    #     html_template = loader.get_template('errors/500.html')
    #     return HttpResponse(html_template.render(context, page))
