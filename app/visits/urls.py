from django.urls import path, re_path
from . import views as visits_views

urlpatterns = [
    path('', visits_views.visits_index, name='index'),
    
    re_path(r'^.*\.*', visits_views.pages, name='pages'),
]
