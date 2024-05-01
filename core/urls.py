from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("app.authentication.urls")),
    path("", include("app.home.urls"))
]
