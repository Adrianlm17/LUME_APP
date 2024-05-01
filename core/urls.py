from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include("app.authentication.urls")),
    path("home/", include("app.home.urls")),
    path('', include('app.visits.urls')),
     
]
