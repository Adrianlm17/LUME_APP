from django.urls import path, re_path
from . import views as home_views


urlpatterns = [
    path('', home_views.home_index, name='home'),
    path('config.html', home_views.edit_profile, name='config'),
    re_path(r'^.*\.*', home_views.pages, name='pages'),
]