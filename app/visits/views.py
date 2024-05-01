from django import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader





def visits_index(request):
    context = {'segment': 'index'}
    return render(request, 'visits/index.html', context)



def pages(request):
    context = {}
    try:

        load_template = request.path.split('/')[-1]

        html_template = loader.get_template('visits/' + load_template)
        return HttpResponse(html_template.render(context, request))


    # ------------------------ EXCEPTS ------------------------
    except template.TemplateDoesNotExist:

        html_template = loader.get_template('errors/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('errors/page-500.html')
        return HttpResponse(html_template.render(context, request))
