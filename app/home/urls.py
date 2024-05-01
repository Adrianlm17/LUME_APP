from django.urls import path, re_path
from . import views as home_views


urlpatterns = [
    path('', home_views.home_index, name='home'),
    re_path(r'^.*\.*', home_views.pages, name='pages'),
]