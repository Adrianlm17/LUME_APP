from django.urls import path
from .views import login_admin_view, login_view, logout_view, register_user

urlpatterns = [
    path('login/', login_view, name="login"),
    path('login_admin/', login_admin_view, name="login_admin"),
    path('register/', register_user, name="register"),
    path('logout/', logout_view, name='logout'),
]
