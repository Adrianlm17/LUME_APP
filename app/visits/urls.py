from django.urls import path, re_path
from . import views as visits_views

urlpatterns = [
    path('', visits_views.visits_index, name='index'),
    path('cambiar_idioma/<str:idioma>/', visits_views.cambiar_idioma, name='cambiar_idioma'),
    re_path(r'^.*\.*', visits_views.pages, name='pages'),
]
