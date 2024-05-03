from django.urls import path, re_path
from . import views as home_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home_views.home_index, name='home'),
    path('config.html', home_views.edit_profile, name='config'),
    re_path(r'^.*\.*', home_views.pages, name='pages'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
