from django.urls import path
from . import views as visits_views

urlpatterns = [
    path('', visits_views.visits_index, name='index'),
    path('info', visits_views.pages, name='info'),
    path('projects', visits_views.pages, name='projects'),
    path('contact', visits_views.pages, name='contact'),
]
