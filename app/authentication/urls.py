from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from .views import login_admin_view, login_view, logout_view, register_user

urlpatterns = [
    path('login/', login_view, name="login"),
    path('login_admin/', login_admin_view, name="login_admin"),
    path('register/', register_user, name="register"),
    path('logout/', logout_view, name='logout'),

    # ---------------------------- RECUPERAR CONTRASEÑA ----------------------------------
    path('reset_password', PasswordResetView.as_view(template_name='accounts/password_reset_form.html', html_email_template_name='accounts/password_reset_email.html'), name='reset_password'),
    path('reset_password_done', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(success_url=reverse_lazy('home:home'), post_reset_login=True, template_name='accounts/password_reset_confirm.html', post_reset_login_backend=('django.contrib.auth.backends.AllowAllUsersModelBackend'),), name='password_reset_confirm'),
]
