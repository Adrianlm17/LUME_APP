from django.urls import path, re_path
from . import views as home_views


app_name = 'home'


urlpatterns = [

    # ------------------------------- INDEX -------------------------------
    path('', home_views.home_index, name='home'),

    # ------------------------------- NOTAS -------------------------------
    path('', home_views.content, name='home'),
    path('index.html', home_views.content, name='home'),
    path('<int:nota_id>/ver_notas', home_views.ver_notas, name='ver_notas'),
    path('<int:nota_id>/delete_nota', home_views.delete_nota, name='delete_nota'),
    path('notas.html', home_views.nota, name='notas'),
    
    # ------------------------------- CHATS -------------------------------
    path('chat.html', home_views.chat, name='chat'),
    path('open_chat', home_views.open_chat, name='open_chat'),
    path('chat/<int:chat_id>/', home_views.chat_detail, name='chat_detail'),

    # ------------------------------- ACTAS -------------------------------
    path('actas.html', home_views.actas, name='actas'),
    path('<int:comunidad_seleccionada>/actas', home_views.actas, name='actas'),
    path('<int:comunidad_seleccionada_id>/crear_acta', home_views.crear_acta, name='crear_acta'),
    path('ver_acta/<int:acta_id>/', home_views.ver_acta, name='ver_acta'),
    path('cambiar_comunidad_acta/<int:comunidad_id>/', home_views.cambiar_comunidad_acta, name='cambiar_comunidad_acta'),

    # ------------------------------- CALENDAR ------------------------------
    path('calendario.html', home_views.calendario, name='calendario_actual'),
    path('<int:año>/<int:mes>/calendario.html', home_views.calendario, name='calendario'),
    path('crear_recordatorio.html', home_views.crear_recordatorio, name='crear_recordatorio'),
    path('detalle_evento/<int:evento_id>/', home_views.detalle_evento, name='detalle_evento'),
    path('<int:recordatorio_id>/delete_calendario', home_views.delete_calendario, name='delete_calendario'),

    # ------------------------------- ANUNCIOS ------------------------------
    path('<int:anuncio_id>/detalles_anuncio', home_views.detalles_anuncio, name='detalles_anuncio'),

    # ------------------------------- GASTOS ------------------------------
    path('gastos', home_views.gastos, name='gastos'),
    path('<int:comunidad_seleccionada>/gastos', home_views.gastos, name='gastos'),
    path('cambiar_comunidad/<int:comunidad_id>/', home_views.cambiar_comunidad, name='cambiar_comunidad'),
    path('<int:comunidad_seleccionada>/crear_gasto/', home_views.crear_gasto, name='crear_gasto'),
    path('<int:comunidad_seleccionada>/crear_recibo/', home_views.crear_recibo, name='crear_recibo'),
    path('<int:comunidad_seleccionada>/crear_motivo/', home_views.crear_motivo, name='crear_motivo'),
    path('<int:recibo_id>/editar_recibo/', home_views.editar_recibo, name='editar_recibo'),
    path('historial_completo/<int:comunidad_id>/', home_views.historial_completo, name='historial_completo'),
    path('ver_historial_individual/<str:tipo>/<int:movimiento_id>/', home_views.ver_historial_individual, name='ver_historial_individual'),
    path('<int:comunidad_seleccionada>/mostrar_modificar_gastos_recibos/', home_views.mostrar_modificar_gastos_recibos, name='mostrar_modificar_gastos_recibos'),
    path('<int:comunidad_seleccionada>/editar_recibo_gasto/<str:tipo>/<int:recibo_id>/', home_views.editar_recibo_gasto, name='editar_recibo_gasto'),
    path('<int:comunidad_seleccionada>/eliminar_recibo_gasto/<str:tipo>/<int:recibo_id>/', home_views.eliminar_recibo_gasto, name='eliminar_recibo_gasto'),

    # ------------------------------- USER CONFIG -------------------------------
    path('config.html', home_views.edit_profile, name='config'),

    # ------------------------------- COMMUNITY CONFIG -------------------------------
    path('comunidades_configuracion', home_views.comunidades_configuracion, name='comunidades_configuracion'),
    path('<int:comunidad_seleccionada>/comunidades_configuracion', home_views.comunidades_configuracion, name='comunidades_configuracion'),
    path('<int:comunidad_seleccionada>/administrar_viviendas', home_views.administrar_viviendas, name='administrar_viviendas'),
    path('<int:comunidad_id>/asignar_usuario_comunidad', home_views.asignar_usuario_comunidad, name='asignar_usuario_comunidad'),
    path('<int:comunidad_id>/<int:viviendas_id>/eliminar_vivienda', home_views.eliminar_vivienda, name='eliminar_vivienda'),
    path('<int:comunidad_id>/<int:viviendas_id>/editar_vivienda_comunidad', home_views.editar_vivienda_comunidad, name='editar_vivienda_comunidad'),

    # ------------------------------- EXTRA -------------------------------
    re_path(r'^.*\.*', home_views.pages, name='pages'),
]
