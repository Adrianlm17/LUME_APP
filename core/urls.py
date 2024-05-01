from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.visits.urls')),
    path("home/", include("app.authentication.urls")),
    path("home/", include("app.home.urls"))
]
