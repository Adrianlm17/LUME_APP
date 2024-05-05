from django.urls import path, re_path
from . import views as admin

app_name = 'admin_lume'

urlpatterns = [
    path('', admin.admin_index, name='admin_lume'),
    
    # ------------------------------- USERS -------------------------------
    path('create_user.html', admin.create_user, name='create_user'),
    path('users.html', admin.user_list, name='user_list'), 
    path('<int:user_id>/edit_user.html', admin.edit_user, name='edit_user'),
    path('<int:user_id>/delete_user', admin.delete_user, name='delete_user'),
    
    # ------------------------------- COMMUNITYS -------------------------------
    path('create_community.html', admin.create_community, name='create_community'),
    path('communitys.html', admin.community_list, name='communitys'), 
    path('<int:communitys_id>/edit_community.html', admin.edit_community, name='edit_community'),
    path('<int:communitys_id>/delete_community', admin.delete_community, name='delete_community'),
    
    # ------------------------------- COMPANY -------------------------------
    path('create_company.html', admin.create_company, name='create_company'),
    path('companys.html', admin.company_list, name='communitys'), 
    path('<int:companys_id>/edit_company.html', admin.edit_company, name='edit_company'),
    path('<int:companys_id>/delete_company', admin.delete_company, name='delete_company'),
    
    # ------------------------------- VIVIENDAS -------------------------------
    path('create_viviendas.html', admin.crear_vivienda, name='create_viviendas'),
    path('viviendas.html', admin.vivienda_list, name='viviendas'), 
    path('<int:viviendas_id>/edit_vivienda.html', admin.edit_vivienda, name='edit_vivienda'),
    path('<int:viviendas_id>/delete_vivienda', admin.delete_vivienda, name='delete_vivienda'),
    
    # ------------------------------- TRABAJADOR -------------------------------
    path('create_worker.html', admin.crear_trabajador, name='create_worker'),
    path('trabajadores.html', admin.trabajador_list, name='trabajadores'), 
    path('<int:trabajadors_id>/edit_trabajador.html', admin.edit_trabajador, name='edit_trabajador'),
    path('<int:trabajadors_id>/delete_trabajador', admin.delete_trabajador, name='delete_trabajador'),
    
    re_path(r'^.*\.*', admin.pages, name='pages'),
]

