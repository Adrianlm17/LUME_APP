import calendar
from django.db.models import Max
from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib import messages
import locale
from django.db.models import Avg
import mimetypes
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import TemplateDoesNotExist, loader
from django.urls import reverse
from app.admin_lume.forms import CrearUserProfileForm
from app.home.forms import ActaForm, AsignarUsuarioComunidadForm, ChatForm, CrearAnuncioForm, EditarComunidadForm, EditarEmpresaForm, EventoForm, ExtendsChatForm, ExtendsGroupChatForm, GastoForm, GroupChatForm, IncidenciaAdminForm, IncidenciaEmpresaForm, IncidenciaForm, MetodoPagoForm, MotivoReciboForm, MotivoReciboFormSet, NotaForm, PagosUsuarioForm, PorcentajePagoForm, ReciboForm, SeguroComunidadForm, UpdateIMGEmpresaForm, UpdateIMGForm, UpdateProfileForm
from app.home.models import Nota, User
from django.db.models import Q
from .models import Acta, Anuncio, Asistencias, Calendario, Chat, ChatReadBy, Comunidad, Empresa, Evento, ExtendsChat, ExtendsGroupChat, Gasto, GroupChat, GroupReadBy, Incidencia, Motivo, Nota, Notificacion, PagosUsuario, Recibo, SeguroComunidad, Trabajador, Transaccion, UserProfile, Vivienda



@login_required(login_url="/login/login/")
def home_index(request):
    hoy = datetime.now()
    fecha_limite = hoy + timedelta(days=15)
    proximos_eventos = Calendario.objects.filter(usuario=request.user, fecha__range=[hoy, fecha_limite]).order_by('fecha')
    notas = Nota.objects.filter(usuario=request.user)
    viviendas_usuario = Vivienda.objects.filter(usuario=request.user)
    comunidades_usuario = [vivienda.comunidad for vivienda in viviendas_usuario]
    anuncios = Anuncio.objects.filter(comunidad__in=comunidades_usuario, fecha_anuncio__range=[hoy, fecha_limite])
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    context = {
        'segment': 'index',
        'notas': notas,
        'proximos_eventos': proximos_eventos,
        'anuncios': anuncios,
        'chats_no_leidos': chats_no_leidos,
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    }

    return render(request, 'home/index.html', context)







@login_required(login_url="/login/login/")
def content(request):
    notas = Nota.objects.filter(usuario=request.user)
    hoy = datetime.now()
    fecha_limite = hoy + timedelta(days=15)
    proximos_eventos = Calendario.objects.filter(usuario=request.user, fecha__range=[hoy, fecha_limite]).order_by('fecha')
    viviendas_usuario = Vivienda.objects.filter(usuario=request.user)
    comunidades_usuario = [vivienda.comunidad for vivienda in viviendas_usuario]
    anuncios = Anuncio.objects.filter(comunidad__in=comunidades_usuario, fecha_anuncio__range=[hoy, fecha_limite])
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    return render(request, 'home/index.html', {'notas': notas, 'segment': 'index', 'proximos_eventos': proximos_eventos, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'anuncios': anuncios, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})



def detalles_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, id=anuncio_id)
    context = {
        'segment': 'index',
        'anuncio': anuncio,
    }
    return render(request, 'home/detalles_anuncio.html', context)



@login_required(login_url="/login/login/")
def pages(request):

    context = {}
    
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))


    # ------------------------ EXCEPTS ------------------------
    except TemplateDoesNotExist:

        html_template = loader.get_template('errors/404.html')
        return HttpResponse(html_template.render(context, request))





# ---------------------------------------------------------- NOTAS ---------------------------------------------------------- 
@login_required(login_url="/login/login/")
def nota(request):
    msg = None
    success = False
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if request.method == 'POST':
        nota_form = NotaForm(request.POST)
        
        if nota_form.is_valid():
            nueva_nota = nota_form.save(commit=False)
            nueva_nota.usuario = request.user
            nueva_nota.save()
            success = True
        else:
            msg = '¡Formulario no válido!'
    else:
        nota_form = NotaForm()

    return render(request, 'home/notas.html', {'segment': 'index', 'nota_form': nota_form, "msg": msg, "success": success, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


def ver_notas(request, nota_id):
    msg = None
    success = False
    notas = get_object_or_404(Nota, id=nota_id)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if request.method == 'POST':
        nota_form = NotaForm(request.POST, instance=notas)
        
        if nota_form.is_valid():
            nueva_nota = nota_form.save(commit=False)
            nueva_nota.usuario = request.user
            nueva_nota.save()
            success = True
        else:
            msg = '¡Formulario no válido!'
    else:
        nota_form = NotaForm(instance=notas)

    return render(request, 'home/ver_notas.html', {'segment': 'index', 'nota_form': nota_form, "msg": msg, "success": success, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def delete_nota(request, nota_id):
    nota_form = get_object_or_404(Nota, id=nota_id)

    if request.method == 'POST':
        nota_form.delete()

    hoy = datetime.now()
    fecha_limite = hoy + timedelta(days=15)
    proximos_eventos = Calendario.objects.filter(usuario=request.user, fecha__range=[hoy, fecha_limite]).order_by('fecha')
    notas_usuario = Nota.objects.filter(usuario=request.user)
    viviendas_usuario = Vivienda.objects.filter(usuario=request.user)
    comunidades_usuario = [vivienda.comunidad for vivienda in viviendas_usuario]
    anuncios = Anuncio.objects.filter(comunidad__in=comunidades_usuario, fecha_anuncio__range=[hoy, fecha_limite])
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    context = {
        'segment': 'index',
        'notas': notas_usuario,
        'proximos_eventos': proximos_eventos,
        'anuncios': anuncios, 
        'chats_no_leidos': chats_no_leidos,
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    }

    return render(request, 'home/index.html', context)





# ---------------------------------------------------------- CHAT ---------------------------------------------------------- 
@login_required(login_url="/login/login/")
def chat(request, user_id=None, grupo_id=None):
    user_chats = Chat.objects.filter(Q(user=request.user) | Q(mensaje_user=request.user))
    users = User.objects.exclude(id=request.user.id)
    group_chats = GroupChat.objects.filter(users__in=[request.user])
    chat = None
    messages = None
    title_form = None
    title_form_grupo = None
    form = None
    group_chat = None
    group_chat_form = GroupChatForm()
    chat_form = ChatForm()

    user_read_chats = ChatReadBy.objects.filter(user=request.user, is_read=True).values_list('chat__id', flat=True)
    
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if request.method == 'POST':
        if 'crear_chat' in request.POST:
            selected_user_id = request.POST.get('selected_user_id')
            if selected_user_id:
                selected_user = get_object_or_404(User, id=selected_user_id)
                existing_chat = Chat.objects.filter(
                    Q(user=request.user, mensaje_user=selected_user) | 
                    Q(user=selected_user, mensaje_user=request.user)
                ).first()

                if existing_chat:
                    return redirect('home:user_chat', user_id=existing_chat.id)
                else:
                    chat = Chat(user=request.user, mensaje_user=selected_user, titulo='Nuevo Chat')
                    chat.save()
                    return redirect('home:user_chat', user_id=chat.id)
        
        elif 'crear_grupo' in request.POST:
            group_chat_form = GroupChatForm(request.POST)
            if group_chat_form.is_valid():
                title = group_chat_form.cleaned_data['title']
                users = group_chat_form.cleaned_data['users']
                group_chat = GroupChat.objects.create(title=title, mensaje_user=request.user)
                group_chat.users.set(users)
                return redirect('home:group_chat', grupo_id=group_chat.id)

    if user_id:
        chat = get_object_or_404(Chat, id=user_id)
        messages = ExtendsChat.objects.filter(chat=chat)
        form = ExtendsChatForm()

        if request.method == 'GET':
            if chat.user:
                chat_read_by, created = ChatReadBy.objects.get_or_create(chat=chat, user=request.user)
                chat_read_by.is_read = True
                chat_read_by.save()

        if request.method == 'POST':
            if 'edit_title' in request.POST:
                title_form = ChatForm(request.POST, instance=chat)
                if title_form.is_valid():
                    title_form.save()
                    return redirect('home:user_chat', user_id=user_id)
            else:
                form = ExtendsChatForm(request.POST)
                if form.is_valid():
                    message = form.save(commit=False)
                    message.chat = chat
                    message.user_send = request.user
                    message.save()
                    chat.last_chat = message.text
                    chat.save()

                    recipient = chat.mensaje_user if chat.user == request.user else chat.user
                    
                    chat_read_by, created = ChatReadBy.objects.get_or_create(chat=chat, user=recipient)
                    chat_read_by.is_read = False
                    chat_read_by.save()

                    return redirect('home:user_chat', user_id=chat.id)
        else:
            title_form = ChatForm(instance=chat)

    elif grupo_id:
        
        group_chat = get_object_or_404(GroupChat, id=grupo_id)
        messages = ExtendsGroupChat.objects.filter(chat=group_chat)
        form = ExtendsGroupChatForm()

        if request.method == 'GET':

            group_read_by, create = GroupReadBy.objects.get_or_create(chat=grupo_id, user=request.user)
            group_read_by.is_read = True
            group_read_by.save()
            
            title_form_grupo = GroupChatForm(initial={'title': group_chat.title})


        elif request.method == 'POST':
            if 'edit_title' in request.POST:
                title_form_grupo = GroupChatForm(request.POST)
                if title_form_grupo.is_valid():
                    group_chat = title_form_grupo.save(commit=False)
                    group_chat.save()
                    return redirect('home:group_chat', grupo_id=grupo_id)

            else:
                form = ExtendsGroupChatForm(request.POST)
                if form.is_valid():
                    message = form.save(commit=False)
                    message.chat = group_chat
                    message.user_send = request.user
                    group_chat.last_chat = message.text  
                    message.save()
                    group_chat.save()

                    recipient_users = group_chat.users.all()
                    for recipient in recipient_users:
                        group_read_by, created = GroupReadBy.objects.get_or_create(chat=group_chat, user=recipient)
                        group_read_by.is_read = False
                        group_read_by.save()

                    return redirect('home:group_chat', grupo_id=grupo_id)


    return render(request, 'home/chat.html', {
        'segment': 'chat',
        'chat': chat,
        'messages': messages,
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
        'title_form': title_form,
        'title_form_grupo':title_form_grupo,
        'grupo_id': grupo_id,
        'user_chats': user_chats,
        'users': users,
        'group_chats': group_chats,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
        'group_chat': group_chat,
        'user_read_chats': user_read_chats,
        'group_chat_form': group_chat_form,
        'chat_form': chat_form,
        'chats_no_leidos': chats_no_leidos,
        'form': form,
    })





@login_required(login_url="/login/login/")
def open_chat(request):
    if request.method == 'POST':
        user_id = request.POST.get('usuario')
        recipient = get_object_or_404(User, id=user_id)

        existing_chat = Chat.objects.filter(user=request.user, mensaje_user=recipient).first()

        if existing_chat:
            chat = existing_chat
        else:
            chat = Chat.objects.create(user=request.user, mensaje_user=recipient)
            chat_read_by, created = ChatReadBy.objects.get_or_create(chat=chat, user=request.user)
            chat_read_by.is_read = True
            chat_read_by.save()

        return redirect('home:user_chat', user_id=chat.id)

    return redirect('home:chat')



@login_required(login_url="/login/login/")
def open_group(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        user_ids = request.POST.getlist('usuarios')
        
        # Crea el grupo de chat con el título proporcionado
        group_chat = GroupChat.objects.create(title=title)
        
        # Agrega los usuarios seleccionados al grupo
        for user_id in user_ids:
            user = get_object_or_404(User, id=user_id)
            group_chat.users.add(user)
        
        group_chat.users.add(request.user)
        
        # Marca el mensaje como leído para todos los usuarios del grupo
        for user in group_chat.users.all():
            group_read_by, created = GroupReadBy.objects.get_or_create(chat=group_chat, user=user)
            group_read_by.is_read = False
            group_read_by.save()
        
        # Redirige a la vista del grupo de chat recién creado
        return redirect('home:group_chat', grupo_id=group_chat.id)

    # Si la solicitud no es de tipo POST, redirige a alguna otra vista, por ejemplo, la vista de chat.
    return redirect('home:chat')






# ---------------------------------------------------------- Incidencias ---------------------------------------------------------- 
@login_required(login_url="/login/login/")
def ver_incidencias(request, comunidad_seleccionada=False):
    user_rol = request.user.userprofile.user_rol
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    # Obtener las comunidades o incidencias según el rol del usuario
    if user_rol in ['community_admin', 'community_user', 'lume']:
        viviendas_usuario = Vivienda.objects.filter(usuario=request.user)
        comunidades = [vivienda.comunidad for vivienda in viviendas_usuario]
    
        if not comunidad_seleccionada:
            if comunidades:
                primera_comunidad = comunidades[0]
                return redirect('home:ver_incidencias', comunidad_seleccionada=primera_comunidad.pk)
        
        else:
            comunidad_seleccionada = Comunidad.objects.get(pk=comunidad_seleccionada)
    
        incidencias = Incidencia.objects.filter(comunidad=comunidad_seleccionada).order_by('-fecha_apertura')
        
        
        return render(request, 'home/incidencias.html', {'segment': 'incidencias', 'chats_no_leidos': chats_no_leidos, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'num_mensajes_no_leidos': num_mensajes_no_leidos, 'incidencias': incidencias, 'comunidades': comunidades, 'comunidad_seleccionada': comunidad_seleccionada})

    else:
        user_trabajador = Trabajador.objects.get(usuario=request.user)
        # Si el usuario es de otro rol, mostrar todas las incidencias asociadas a su empresa
        incidencias = Incidencia.objects.filter(empresa=user_trabajador.empresa).order_by('-fecha_apertura')
        return render(request, 'home/incidencias.html', {'segment': 'incidencias', 'chats_no_leidos': chats_no_leidos, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'num_mensajes_no_leidos': num_mensajes_no_leidos, 'incidencias': incidencias})


@login_required(login_url="/login/login/")
def cambiar_comunidad_incidencias(request, comunidad_id):
    if request.method == 'POST':
        nueva_comunidad_id = request.POST.get('comunidad_id')
        request.session['comunidad_id'] = nueva_comunidad_id
        return redirect('home:ver_incidencias', comunidad_seleccionada=nueva_comunidad_id)
    else:
        return redirect(reverse('home:ver_incidencias'))

    
@login_required(login_url="/login/login/")
def crear_incidencia(request, comunidad_seleccionada):
    comunidad = get_object_or_404(Comunidad, pk=comunidad_seleccionada)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if request.method == 'POST':
        incidencia_form = IncidenciaForm(request.POST, request.FILES)
        if incidencia_form.is_valid():
            incidencia = incidencia_form.save(commit=False)
            incidencia.usuario = request.user
            incidencia.comunidad = comunidad
            incidencia.save()
            return redirect('home:ver_incidencias', comunidad_seleccionada=comunidad_seleccionada)
    else:
        incidencia_form = IncidenciaForm()

    return render(request, 'home/crear_incidencia.html', {
        'segment': 'incidencias', 
        'chats_no_leidos': chats_no_leidos, 
        'num_mensajes_no_leidos': num_mensajes_no_leidos, 
        'incidencia_form': incidencia_form,
        'notificaciones_no_leidas': notificaciones_no_leidas, 
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    })


@login_required(login_url="/login/login/")
def editar_incidencia(request, numero):
    incidencia = get_object_or_404(Incidencia, pk=numero)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()
    
    if request.method == 'POST':
        incidencia_form = IncidenciaAdminForm(request.POST, request.FILES, instance=incidencia)
        
        if incidencia_form.is_valid():
            incidencia = incidencia_form.save(commit=False)
            jefe_notificado = False  # Para asegurarnos de que solo se notifique una vez
            presidente_notificado = False  # Para asegurarnos de que solo se notifique una vez

            if incidencia.estado == 'Asignada' and incidencia.empresa:
                empresa = incidencia.empresa
                jefe = Trabajador.objects.filter(empresa=empresa, usuario__userprofile__user_rol='company_boss').first()
                if jefe and not jefe_notificado:
                    jefe_notificado = True
                    # Crear notificación para el jefe de la empresa
                    notificacion = Notificacion(
                        user=jefe.usuario,
                        mensaje=incidencia.titulo,
                        url=f"/home/{incidencia.numero}/ver_incidencia"
                    )
                    notificacion.save()
                    # Crear el chat con el jefe de la empresa
                    chat, created = Chat.objects.get_or_create(user=request.user, mensaje_user=jefe.usuario)
                    chat_read_by, _ = ChatReadBy.objects.get_or_create(chat=chat, user=request.user)
                    chat.titulo = f"Incidencia #{incidencia.numero}"  # Establecer el título del chat
                    chat.save()
                    chat_read_by.is_read = True
                    chat_read_by.save()

            if incidencia.estado == 'Finalizada':
                empresa = incidencia.empresa
                valoracion_media_nueva = Incidencia.objects.filter(empresa=empresa, estado='Finalizada').aggregate(avg_valoracion=Avg('valoracion'))['avg_valoracion']
                if valoracion_media_nueva is not None:
                    empresa.valoracion_media = Decimal(str(valoracion_media_nueva))
                    empresa.save()

                if incidencia.gasto:
                    comunidad = incidencia.comunidad
                    comunidad.dinero -= incidencia.gasto
                    comunidad.save()
                
                incidencia.fecha_cierre = timezone.now()

            if incidencia.prioridad in ['Alta', 'Urgente'] and incidencia.estado != incidencia_form.initial['estado']:
                comunidad = incidencia.comunidad
                presidente = Trabajador.objects.filter(comunidad=comunidad, usuario__userprofile__user_rol='community_president').first()
                if presidente and not presidente_notificado:
                    presidente_notificado = True
                    notificacion = Notificacion(
                        user=presidente.usuario,
                        mensaje=f"El estado de una incidencia de alta prioridad ha cambiado: {incidencia.titulo}",
                        url=f"/home/{incidencia.numero}/ver_incidencia"
                    )
                    notificacion.save()

            incidencia.save()
            
            return redirect('home:ver_incidencias')
    else:
        incidencia_form = IncidenciaAdminForm(instance=incidencia)
    
    return render(request, 'home/editar_incidencia.html', {
        'segment': 'incidencias',
        'chats_no_leidos': chats_no_leidos,
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
        'incidencia_form': incidencia_form,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    })



@login_required(login_url="/login/login/")
def editar_incidencia_empresa(request, numero):
    incidencia = get_object_or_404(Incidencia, pk=numero)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()
    
    if request.method == 'POST':
        incidencia_form = IncidenciaEmpresaForm(request.POST, request.FILES, instance=incidencia)
        
        if incidencia_form.is_valid():
            incidencia = incidencia_form.save(commit=False)
            incidencia.empresa = incidencia.empresa
            incidencia.valoracion = incidencia.valoracion
            incidencia.prioridad = incidencia.prioridad
            incidencia.save()
            return redirect('home:ver_incidencias')
    else:
        incidencia_form = IncidenciaEmpresaForm(instance=incidencia)
    
    return render(request, 'home/editar_incidencia_empresa.html', {'segment': 'incidencias', 'chats_no_leidos': chats_no_leidos, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'num_mensajes_no_leidos': num_mensajes_no_leidos, 'incidencia_form': incidencia_form})



@login_required(login_url="/login/login/")
def ver_incidencia(request, numero):
    # Obtener la incidencia específica por su ID
    incidencia = get_object_or_404(Incidencia, pk=numero)
    
    # Marcar las notificaciones asociadas con la incidencia específica como leídas
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False, mensaje=incidencia.titulo)
    for notificacion in notificaciones_no_leidas:
        notificacion.leida = True
        notificacion.save()

    # Obtener chats no leídos y contarlos
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    
    # Contar el número de notificaciones no leídas
    num_notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False).count()
    
    # Verificar si hay un archivo adjunto para descargar
    if incidencia.archivo and request.GET.get('download') == 'true':
        # Abrir el archivo en modo binario
        with open(incidencia.archivo.path, 'rb') as file:
            contenido = file.read()

        # Obtener el tipo MIME del archivo
        tipo_contenido, _ = mimetypes.guess_type(incidencia.archivo.path)

        # Configurar la respuesta HTTP
        response = HttpResponse(contenido, content_type=tipo_contenido)
        response['Content-Disposition'] = f'attachment; filename="{incidencia.archivo.name}"'

        # Devolver la respuesta
        return response
    else:
        # Si no hay archivo o no se solicita la descarga, simplemente renderizar la plantilla con los detalles de la incidencia
        return render(request, 'home/ver_incidencia.html', {
            'segment': 'incidencias',
            'chats_no_leidos': chats_no_leidos,
            'notificaciones_no_leidas': notificaciones_no_leidas,
            'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
            'num_mensajes_no_leidos': num_mensajes_no_leidos,
            'incidencia': incidencia
        })


@login_required(login_url="/login/login/")
def ver_empresas(request):
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()
    
    query = request.GET.get('q')
    if query:
        empresas = Empresa.objects.filter(
            Q(nombre__icontains=query) | 
            Q(tags__name__icontains=query)
        ).distinct().order_by('-valoracion_media')
    else:
        empresas = Empresa.objects.all().order_by('-valoracion_media')
    
    return render(request, 'home/ver_empresas.html', {
        'segment': 'incidencias',
        'chats_no_leidos': chats_no_leidos,
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
        'empresas': empresas,
        'query': query,
        'notificaciones_no_leidas': notificaciones_no_leidas, 
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    })


@login_required(login_url="/login/login/")
def mapa_empresas(request):
    # Obtener las provincias de las comunidades a las que pertenece el usuario
    provincias_usuario = Vivienda.objects.filter(usuario=request.user).values_list('comunidad__provincia', flat=True).distinct()

    # Obtener las comunidades y empresas en las provincias del usuario
    comunidades = Vivienda.objects.filter(usuario=request.user).values_list('comunidad', flat=True).distinct()
    empresas = Empresa.objects.filter(provincia__in=provincias_usuario)

    return render(request, 'home/mapa_empresas.html', {
        'comunidades': comunidades,
        'empresas': empresas,
    })


def detalle_empresa(request, empresa_id):
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()
    
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    incidencias = Incidencia.objects.filter(empresa=empresa)
    return render(request, 'home/detalle_empresa.html', {
        'segment': 'incidencias',
        'chats_no_leidos': chats_no_leidos,
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
        'empresa': empresa,
        'incidencias': incidencias,
        'notificaciones_no_leidas': notificaciones_no_leidas, 
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    })




# ---------------------------------------------------------- ACTAS ---------------------------------------------------------- 
@login_required(login_url="/login/login/")
def actas(request, comunidad_seleccionada=False):
    viviendas_usuario = Vivienda.objects.filter(usuario=request.user)
    comunidades = [vivienda.comunidad for vivienda in viviendas_usuario]
    
    if not comunidad_seleccionada:
        if comunidades:
            primera_comunidad = comunidades[0]
            return redirect('home:actas', comunidad_seleccionada=primera_comunidad.pk)
        else:
            pass
    else:
        comunidad_seleccionada = Comunidad.objects.get(pk=comunidad_seleccionada)
    
    actas_usuario = Acta.objects.filter(comunidad=comunidad_seleccionada)

    es_presidente_o_vicepresidente = any(
        vivienda.rol_comunidad in ['community_president', 'community_vicepresident'] for vivienda in viviendas_usuario
    )

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    return render(request, 'home/actas.html', {'segment': 'actas', 'comunidades': comunidades, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'comunidad_seleccionada': comunidad_seleccionada, 'actas_usuario': actas_usuario, 'es_presidente_o_vicepresidente': es_presidente_o_vicepresidente, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def cambiar_comunidad_actas(request, comunidad_id):
    if request.method == 'POST':
        nueva_comunidad_id = request.POST.get('comunidad_id')
        request.session['comunidad_id'] = nueva_comunidad_id
        return redirect('home:actas', comunidad_seleccionada=nueva_comunidad_id)
    else:
        return redirect(reverse('home:actas'))


@login_required(login_url="/login/login/")
def crear_acta(request, comunidad_seleccionada_id):
    comunidad = get_object_or_404(Comunidad, pk=comunidad_seleccionada_id)
    if request.method == 'POST':
        acta_form = ActaForm(request.POST, request.FILES)
        if acta_form.is_valid():
            acta = acta_form.save(commit=False)
            acta.firmada = request.user
            acta.fecha = timezone.now()
            acta.comunidad = comunidad
            acta.save()
            return redirect('home:actas')
    else:
        acta_form = ActaForm()

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    return render(request, 'home/crear_acta.html', {'segment': 'actas', 'acta_form': acta_form, 'chats_no_leidos': chats_no_leidos, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def ver_acta(request, acta_id):
    acta = get_object_or_404(Acta, id=acta_id)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if acta.archivo and request.GET.get('download') == 'true':
        # Abrir el archivo en modo binario
        with open(acta.archivo.path, 'rb') as file:
            contenido = file.read()

        # Obtener el tipo MIME del archivo
        tipo_contenido, _ = mimetypes.guess_type(acta.archivo.path)

        # Configurar la respuesta HTTP
        response = HttpResponse(contenido, content_type=tipo_contenido)
        response['Content-Disposition'] = f'attachment; filename="{acta.archivo.name}"'

        # Devolver la respuesta
        return response
    
    return render(request, 'home/ver_acta.html', {'segment': 'actas', 'acta': acta, 'chats_no_leidos': chats_no_leidos, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'num_mensajes_no_leidos':num_mensajes_no_leidos})






# ---------------------------------------------------------- CALENDAR ---------------------------------------------------------
def calendario(request, año=None, mes=None):
    hoy = datetime.now()
    if año is None or mes is None:
        año = hoy.year
        mes = hoy.month
    else:
        año = int(año)
        mes = int(mes)

    meses_espanol = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
        7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    
    titulo = f"{(meses_espanol[mes]).capitalize()} | {año}"
    eventos_mes_actual = Calendario.objects.filter(fecha__year=año, fecha__month=mes, usuario=request.user)
    
    calendario_mes = []
    for semana in calendar.monthcalendar(año, mes):
        semana_calendario = []
        for dia in semana:
            if dia == 0:
                semana_calendario.append((None, None))
            else:
                recordatorios_dia = eventos_mes_actual.filter(fecha__day=dia)
                semana_calendario.append((dia, recordatorios_dia))
        calendario_mes.append(semana_calendario)

    mes_anterior = mes - 1 if mes > 1 else 12
    año_anterior = año - 1 if mes == 1 else año
    mes_siguiente = mes + 1 if mes < 12 else 1
    año_siguiente = año + 1 if mes == 12 else año
    url_mes_anterior = reverse('home:calendario', kwargs={'año': año_anterior, 'mes': mes_anterior})
    url_mes_siguiente = reverse('home:calendario', kwargs={'año': año_siguiente, 'mes': mes_siguiente})

    dias_de_la_semana = [('Lunes'), ('Martes'), ('Miércoles'), ('Jueves'), ('Viernes'), ('Sábado'), ('Domingo')]

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    return render(request, 'home/calendario.html', {
        'segment': 'calendario',
        'titulo': titulo,
        'calendario_mes': calendario_mes,
        'dias_de_la_semana': dias_de_la_semana,
        'url_mes_anterior': url_mes_anterior,
        'url_mes_siguiente': url_mes_siguiente, 
        'chats_no_leidos': chats_no_leidos, 
        'num_mensajes_no_leidos':num_mensajes_no_leidos,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    })


@login_required(login_url="/login/login/")
def crear_recordatorio(request):
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        
        recordatorio = Calendario(usuario=request.user, titulo=titulo, descripcion=descripcion, fecha=fecha)
        recordatorio.save()
        
        hoy = datetime.now()
        año = hoy.year
        mes = hoy.month

        return redirect('home:calendario', año=año, mes=mes)
    else:
        return render(request, 'home/crear_recordatorio.html', {'segment': 'calendario', 'chats_no_leidos': chats_no_leidos, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def detalle_evento(request, evento_id):
    evento = get_object_or_404(Calendario, id=evento_id)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if request.method == 'POST':
        evento.titulo = request.POST.get('titulo')
        evento.descripcion = request.POST.get('descripcion')
        evento.save()
        return redirect('home:detalle_evento', evento_id=evento.id)
    
    return render(request, 'home/detalle_evento.html', {'segment': 'calendario', 'evento': evento, 'chats_no_leidos': chats_no_leidos, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def delete_calendario(request, recordatorio_id):
    recordatorio_form = get_object_or_404(Calendario, id=recordatorio_id)

    if request.method == 'POST':
        recordatorio_form.delete()

    hoy = datetime.now()
    año = hoy.year
    mes = hoy.month

    return redirect('home:calendario', año=año, mes=mes)






# ---------------------------------------------------------- EVENTOS ---------------------------------------------------------- 
@login_required(login_url="/login/login/")
def eventos(request):
    now = timezone.now()
    
    # Obtener las comunidades a las que pertenece el usuario a través de sus viviendas
    user_communities = Comunidad.objects.filter(vivienda__usuario=request.user).distinct()
    
    # Obtener la provincia de las comunidades del usuario
    user_provinces = user_communities.values_list('provincia', flat=True).distinct()
    
    # Eventos de las comunidades del usuario (privados y públicos)
    community_events = Evento.objects.filter(
        Q(comunidad__in=user_communities) &
        Q(date__gte=now)
    ).distinct()

    # Eventos públicos en las mismas provincias que las comunidades del usuario
    other_public_events = Evento.objects.filter(
        Q(visibility=Evento.PUBLIC) &
        Q(date__gte=now) &
        Q(comunidad__provincia__in=user_provinces)
    ).exclude(comunidad__in=user_communities).distinct()

    community_events_with_attendance = {}
    for evento in community_events:
        is_attending = Asistencias.objects.filter(evento=evento, usuario=request.user).exists()
        community_events_with_attendance[evento] = is_attending

    other_public_events_with_attendance = {}
    for evento in other_public_events:
        is_attending = Asistencias.objects.filter(evento=evento, usuario=request.user).exists()
        other_public_events_with_attendance[evento] = is_attending

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    return render(request, 'home/eventos.html', {
        'segment': 'eventos',
        'community_events_with_attendance': community_events_with_attendance,
        'other_public_events_with_attendance': other_public_events_with_attendance,
        'chats_no_leidos': chats_no_leidos, 
        'notificaciones_no_leidas': notificaciones_no_leidas, 
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 
        'num_mensajes_no_leidos': num_mensajes_no_leidos
    })




@login_required(login_url="/login/login/")
def crear_evento(request):
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.usuario = request.user
            evento.save()
            return redirect('home:eventos')
    else:
        form = EventoForm(user=request.user)
    return render(request, 'home/crear_evento.html', {'segment': 'eventos', 'form': form, 'chats_no_leidos': chats_no_leidos, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def unirse_evento(request, event_id):
    evento = get_object_or_404(Evento, id=event_id)
    if evento.current_attendees < evento.max_attendees:

        if Asistencias.objects.filter(evento=evento, usuario=request.user).exists():
            messages.error(request, 'Ya estás inscrito en este evento!')
        else:
            Asistencias.objects.create(evento=evento, usuario=request.user)
            evento.current_attendees += 1
            evento.save()

            Calendario.objects.create(
                usuario=request.user,
                titulo=evento.title,
                descripcion=evento.descripcion,
                fecha=evento.date
            )

            messages.success(request, 'Fuiste apuntad@ correctamente al evento!')
    else:
        messages.error(request, 'El evento está completo...')

    return redirect('home:eventos')


@login_required(login_url="/login/login/")
def desapuntarse_evento(request, event_id):
    evento = get_object_or_404(Evento, id=event_id)
    attendance = Asistencias.objects.filter(evento=evento, usuario=request.user)
    
    if attendance.exists():
        attendance.delete()
        evento.current_attendees -= 1
        evento.save()

        Calendario.objects.filter(usuario=request.user, titulo=evento.title, fecha=evento.date).delete()
        
        messages.success(request, '¡Te has desapuntado del evento!')
    else:
        messages.error(request, 'No estabas apuntado a este evento...')

    return redirect('home:eventos')




# ---------------------------------------------------------- GASTOS ---------------------------------------------------------- 
@login_required(login_url="/login/login/")
def gastos(request, comunidad_seleccionada=False):
    user_profile = UserProfile.objects.get(user=request.user)
    viviendas_usuario = Vivienda.objects.filter(usuario=request.user)
    comunidades = [vivienda.comunidad for vivienda in viviendas_usuario]
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    es_presidente_o_vicepresidente = False

    if not comunidad_seleccionada:
        if comunidades:
            primera_comunidad = comunidades[0]
            return redirect('home:gastos', comunidad_seleccionada=primera_comunidad.pk)
    else:
        es_presidente_o_vicepresidente = Vivienda.objects.filter(usuario=request.user, comunidad=comunidad_seleccionada, rol_comunidad__in=['community_president', 'community_vicepresident']).exists()

        # Obtener la comunidad seleccionada
        comunidad_seleccionada = Comunidad.objects.get(pk=comunidad_seleccionada)

        # Obtener el dinero actual de la comunidad
        dinero_actual_comunidad = comunidad_seleccionada.dinero

        # Obtener la fecha del próximo recibo pendiente
        proximo_recibo_pendiente = obtener_proximo_recibo_pendiente(comunidad_seleccionada)

        # Obtener el historial del dinero de la comunidad
        historial_dinero_mensual_comunidad = obtener_historial_mensual_dinero_comunidad(comunidad_seleccionada)
        historial_dinero_comunidad = obtener_historial_dinero_comunidad(comunidad_seleccionada, request.user)

        # Obtener la distribución de gastos del último recibo
        distribucion_gastos_ultimo_recibo = obtener_distribucion_gastos_ultimo_recibo(comunidad_seleccionada)

        proximos_pagos = obtener_proximos_pagos_usuario(request.user, comunidad_seleccionada)
        
        mis_pagos = obtener_mis_pagos_usuario(request.user, comunidad_seleccionada)

        seguro_comunidad = SeguroComunidad.objects.filter(comunidad=comunidad_seleccionada).first()
        
        return render(request, 'home/gastos.html', {'segment': 'gastos', 'chats_no_leidos': chats_no_leidos, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'num_mensajes_no_leidos':num_mensajes_no_leidos, 'user_profile': user_profile, 'comunidades': comunidades, 'comunidad_seleccionada': comunidad_seleccionada, 'dinero_actual_comunidad': dinero_actual_comunidad, 'proximo_recibo_pendiente': proximo_recibo_pendiente, 'historial_dinero_mensual_comunidad': historial_dinero_mensual_comunidad, 'historial_dinero_comunidad': historial_dinero_comunidad, 'distribucion_gastos_ultimo_recibo': distribucion_gastos_ultimo_recibo, 'proximos_pagos': proximos_pagos, 'mis_pagos': mis_pagos, 'es_presidente_o_vicepresidente': es_presidente_o_vicepresidente, "seguro_comunidad": seguro_comunidad})


def obtener_historial_mensual_dinero_comunidad(comunidad):
    historial = []

    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    
    # Obtener todos los recibos de la comunidad para el año actual
    recibos = Recibo.objects.filter(comunidad=comunidad, fecha__year=timezone.now().year)
    
    # Iterar sobre cada recibo para obtener la información relevante
    for recibo in recibos:
        mes = calendar.month_name[recibo.fecha.month]
        historial.append({
            'mes': mes,
            'tipo': 'Recibo',
            'titulo': recibo.titulo,
            'fecha': recibo.fecha,
            'cantidad': recibo.cantidad_total
        })
    
    return historial


def obtener_historial_dinero_comunidad(comunidad, usuario):
    historial = []

    # Obtener todos los gastos de la comunidad para el año actual
    gastos_comunidad = Gasto.objects.filter(comunidad=comunidad, fecha__year=timezone.now().year, usuario=None).order_by('-id')[:2]
    
    # Iterar sobre cada gasto de la comunidad
    for gasto in gastos_comunidad:
        historial.append({
            'tipo': 'Gasto Comunidad',
            'titulo': gasto.titulo,
            'fecha': gasto.fecha,
            'cantidad': gasto.cantidad_total,
            'estado': gasto.estado
        })

    # Obtener todos los gastos personales del usuario para el año actual
    gastos_personales = PagosUsuario.objects.filter(usuario=usuario, comunidad=comunidad).order_by('-id')[:2]
    
    # Iterar sobre cada gasto personal del usuario
    for gasto_personal in gastos_personales:
        historial.append({
            'tipo': 'Gasto Personal',
            'titulo': gasto_personal.titulo,
            'fecha': gasto_personal.fecha,
            'cantidad': gasto_personal.cantidad,
            'estado': gasto_personal.estado
        })
    
    return historial


def obtener_proximo_recibo_pendiente(comunidad):
    try:
        ultimo_recibo = Recibo.objects.filter(comunidad=comunidad).latest('fecha_tope')
        return ultimo_recibo.fecha_tope.strftime("%Y-%m-%d")
    except:
        return "No hay recibo pendiente"



def obtener_distribucion_gastos_ultimo_recibo(comunidad):
    try:
        # Obtener el último recibo
        ultimo_recibo = Recibo.objects.filter(comunidad=comunidad).latest('fecha')
        
        # Obtener todos los tipos de gastos posibles
        tipos_gastos = ['luz', 'agua', 'gas', 'piscina', 'jardineria', 'personal', 'limpieza', 'seguro','fondos','extras']

        # Inicializar el diccionario de distribución con todos los tipos de gastos y cantidades en 0
        distribucion = {tipo: 0 for tipo in tipos_gastos}
        
        # Obtener los motivos del último recibo y actualizar la distribución
        motivos_recibo = Motivo.objects.filter(recibo=ultimo_recibo)
        for motivo in motivos_recibo:
            distribucion[motivo.tipo] = motivo.cantidad
        
        return distribucion
    except:
        # Si no hay recibo disponible, devolver un diccionario vacío
        return {}
    

def obtener_proximos_pagos_usuario(usuario, comunidad):
    try:
        return PagosUsuario.objects.filter(usuario=usuario, comunidad=comunidad, fecha__gte=datetime.now()).order_by('fecha')
    except:
        return []



def obtener_mis_pagos_usuario(usuario, comunidad):
    try:
        return PagosUsuario.objects.filter(usuario=usuario, comunidad=comunidad)
    except:
        return []
    

def obtener_historial_completo(comunidad, usuario):
    historial_completo = []

    # Obtener todos los gastos de la comunidad
    gastos_comunidad = Gasto.objects.filter(comunidad=comunidad)
    for gasto in gastos_comunidad:
        historial_completo.append({'tipo': 'Gasto', 'id': gasto.id, 'fecha': gasto.fecha_tope, 'titulo': gasto.titulo, 'descripcion': gasto.descripcion, 'cantidad_total': gasto.cantidad_total})

    # Obtener todos los gastos personales del usuario
    gastos_personales = PagosUsuario.objects.filter(usuario=usuario)
    for gasto_personal in gastos_personales:
        historial_completo.append({'tipo': 'Gasto Personal', 'id': gasto_personal.id, 'fecha': gasto_personal.fecha, 'titulo': gasto_personal.titulo, 'descripcion': gasto_personal.descripcion, 'cantidad_total': gasto_personal.cantidad})

    # Ordenar el historial por fecha en orden descendente
    historial_completo.sort(key=lambda x: x['fecha'], reverse=True)

    return historial_completo


@login_required(login_url="/login/login/")
def historial_completo(request, comunidad_id):
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()
    
    # Obtener la comunidad
    comunidad = Comunidad.objects.get(pk=comunidad_id)
    
    # Obtener el historial completo de la comunidad
    historial_completo = obtener_historial_completo(comunidad, request.user)

    return render(request, 'home/historial_completo.html', {'segment': 'gastos', 'comunidad': comunidad, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'historial_completo': historial_completo, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def ver_historial_individual(request, tipo, movimiento_id):
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if tipo == 'gasto':
        movimiento = get_object_or_404(Gasto, pk=movimiento_id)
    elif tipo == 'gasto_personal':
        movimiento = get_object_or_404(PagosUsuario, pk=movimiento_id)
    else:
        pass
    
    if movimiento.archivo and request.GET.get('download') == 'true':
        # Abrir el archivo en modo binario
        with open(movimiento.archivo.path, 'rb') as file:
            contenido = file.read()

        # Obtener el tipo MIME del archivo
        tipo_contenido, _ = mimetypes.guess_type(movimiento.archivo.path)

        # Configurar la respuesta HTTP
        response = HttpResponse(contenido, content_type=tipo_contenido)
        response['Content-Disposition'] = f'attachment; filename="{movimiento.archivo.name}"'

        # Devolver la respuesta
        return response
    
    return render(request, 'home/ver_historial_individual.html', {'segment': 'gastos', 'tipo':tipo, 'movimiento': movimiento, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def cambiar_comunidad_gastos(request, comunidad_id):
    if request.method == 'POST':
        nueva_comunidad_id = request.POST.get('comunidad_id')
        request.session['comunidad_id'] = nueva_comunidad_id
        return redirect('home:gastos', comunidad_seleccionada=nueva_comunidad_id)
    else:
        return redirect(reverse('home:gastos'))



@login_required(login_url="/login/login/")
def crear_gasto(request, comunidad_seleccionada):
    comunidad = Comunidad.objects.get(pk=comunidad_seleccionada)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    # Obtener los usuarios que tienen viviendas en la comunidad seleccionada
    usuarios_comunidad = User.objects.filter(vivienda__comunidad=comunidad)

    if request.method == 'POST':
        gasto_form = GastoForm(request.POST, request.FILES, usuarios_comunidad=usuarios_comunidad)
        
        if gasto_form.is_valid():
            gasto = gasto_form.save(commit=False)
            gasto.comunidad = comunidad
            gasto.save()

            # Obtener el usuario asignado si tiene
            usuario_id = request.POST.get('usuario')
            
            if usuario_id:
                usuario = User.objects.get(pk=usuario_id)
                saldo_actual = usuario.userprofile.saldo

                if saldo_actual >= gasto.cantidad_total:
                    usuario.userprofile.saldo -= gasto.cantidad_total
                    usuario.userprofile.save()
                    estado = 'pagado'
                else:
                    gasto.cantidad_total = gasto.cantidad_total - saldo_actual
                    usuario.userprofile.saldo = 0
                    usuario.userprofile.save()
                    estado = 'pendiente'

                PagosUsuario.objects.create(
                    usuario=usuario,
                    comunidad=comunidad,
                    titulo=gasto.titulo,
                    descripcion=gasto.descripcion,
                    fecha=gasto.fecha_tope,
                    cantidad=gasto.cantidad_total,
                    estado=estado,
                    archivo=gasto.archivo
                )

                Calendario.objects.create(
                    usuario=usuario,
                    titulo=f"Gasto: {gasto.titulo}",
                    descripcion=gasto.descripcion,
                    fecha=gasto.fecha_tope
                )

            else:
                # Calcular la cantidad que cada miembro de la comunidad debe pagar
                total_gasto = gasto.cantidad_total
                viviendas_comunidad = Vivienda.objects.filter(comunidad=comunidad)
                numero_viviendas = viviendas_comunidad.count()
                cantidad_por_vivienda = total_gasto / numero_viviendas

                # Crear un registro de pago para cada usuario de cada vivienda en la comunidad
                for vivienda in viviendas_comunidad:
                    usuario = vivienda.usuario
                    saldo_actual = usuario.userprofile.saldo

                    if saldo_actual >= cantidad_por_vivienda:
                        usuario.userprofile.saldo -= cantidad_por_vivienda
                        usuario.userprofile.save()
                        estado = 'pagado'
                    else:
                        usuario.userprofile.saldo = 0
                        usuario.userprofile.save()
                        estado = 'pendiente'
                        cantidad_por_vivienda = cantidad_por_vivienda - saldo_actual

                    PagosUsuario.objects.create(
                        usuario=usuario,
                        comunidad=comunidad,
                        titulo=gasto.titulo,
                        descripcion=gasto.descripcion,
                        fecha=gasto.fecha_tope,
                        cantidad=cantidad_por_vivienda,
                        estado=estado,
                        archivo=gasto.archivo
                    )

                    Calendario.objects.create(
                        usuario=usuario,
                        titulo=f"Gasto: {gasto.titulo}",
                        descripcion=gasto.descripcion,
                        fecha=gasto.fecha_tope
                    )

                comunidad.dinero_actual -= total_gasto
                comunidad.save()

                Transaccion.objects.create(
                    comunidad=comunidad,
                    monto=-total_gasto,
                    descripcion=f"Gasto: {gasto.titulo}"
                )

            # Eliminar el gasto general después de crear los pagos personales
            gasto.delete()

            return redirect('home:gastos')
    else:
        gasto_form = GastoForm(usuarios_comunidad=usuarios_comunidad)

    return render(request, 'home/crear_gasto.html', {
        'segment': 'gastos',
        'gasto_form': gasto_form,
        'comunidad': comunidad, 
        'chats_no_leidos': chats_no_leidos, 
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    })






@login_required(login_url="/login/login/")
def crear_recibo(request, comunidad_seleccionada):
    comunidad = get_object_or_404(Comunidad, pk=comunidad_seleccionada)

    if request.method == 'POST':
        recibo_form = ReciboForm(request.POST, request.FILES)
        motivo_recibo_formset = MotivoReciboFormSet(request.POST)

        if recibo_form.is_valid() and motivo_recibo_formset.is_valid():
            recibo = recibo_form.save(commit=False)
            recibo.comunidad = comunidad
            recibo.save()

            # Obtener el método de pago de la comunidad
            metodo_pago = comunidad.metodo_pago

            # Calcular la cantidad que cada miembro de la comunidad debe pagar
            total_recibo = recibo.cantidad_total
            viviendas_comunidad = Vivienda.objects.filter(comunidad=comunidad)
            numero_viviendas = viviendas_comunidad.count()

            if metodo_pago == 'igual':
                cantidad_por_usuario = total_recibo / numero_viviendas
                for vivienda in viviendas_comunidad:
                    usuario = vivienda.usuario
                    saldo_actual = usuario.userprofile.saldo

                    if saldo_actual >= cantidad_por_usuario:
                        usuario.userprofile.saldo -= cantidad_por_usuario
                        usuario.userprofile.save()
                        estado = 'pagado'
                    else:
                        usuario.userprofile.saldo = 0
                        usuario.userprofile.save()
                        estado = 'pendiente'
                        cantidad_por_usuario = cantidad_por_usuario - saldo_actual

                    PagosUsuario.objects.create(
                        usuario=usuario,
                        comunidad=comunidad,
                        titulo=recibo.titulo,
                        descripcion=recibo.descripcion,
                        fecha=recibo.fecha_tope,
                        cantidad=cantidad_por_usuario,
                        estado=estado,
                        archivo=recibo.archivo
                    )
            else:  # método_pago == 'porcentajes'
                total_porcentajes = sum(vivienda.porcentaje_pago for vivienda in viviendas_comunidad)
                for vivienda in viviendas_comunidad:
                    cantidad_por_usuario = total_recibo * vivienda.porcentaje_pago / total_porcentajes
                    usuario = vivienda.usuario
                    saldo_actual = usuario.userprofile.saldo

                    if saldo_actual >= cantidad_por_usuario:
                        usuario.userprofile.saldo -= cantidad_por_usuario
                        usuario.userprofile.save()
                        estado = 'pagado'
                    else:
                        usuario.userprofile.saldo = 0
                        usuario.userprofile.save()
                        estado = 'pendiente'
                        cantidad_por_usuario = cantidad_por_usuario - saldo_actual

                    PagosUsuario.objects.create(
                        usuario=usuario,
                        comunidad=comunidad,
                        titulo=recibo.titulo,
                        descripcion=recibo.descripcion,
                        fecha=recibo.fecha_tope,
                        cantidad=cantidad_por_usuario,
                        estado=estado,
                        archivo=recibo.archivo
                    )

            comunidad.dinero -= total_recibo
            comunidad.save()

            Transaccion.objects.create(
                comunidad=comunidad,
                monto=-total_recibo,
                descripcion=f"Recibo: {recibo.titulo}"
            )

            return redirect('home:crear_motivo', comunidad_seleccionada=comunidad_seleccionada)

    else:
        recibo_form = ReciboForm()
        motivo_recibo_formset = MotivoReciboFormSet()

    motivos_recibo = Recibo.objects.filter(comunidad=comunidad).order_by('-id').first().motivos.all() if Recibo.objects.filter(comunidad=comunidad) else None

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    return render(request, 'home/crear_recibo.html', {
        'segment': 'gastos',
        'recibo_form': recibo_form,
        'motivo_recibo_formset': motivo_recibo_formset,
        'comunidad': comunidad,
        'motivos_recibo': motivos_recibo,
        'chats_no_leidos': chats_no_leidos,
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    })





@login_required(login_url="/login/login/")
def crear_motivo(request, comunidad_seleccionada):
    comunidad = Comunidad.objects.get(pk=comunidad_seleccionada)

    # Obtener el recibo más reciente creado
    recibo = Recibo.objects.filter(comunidad=comunidad).order_by('-id').first()

    if request.method == 'POST':
        motivo_form = MotivoReciboForm(request.POST)
        if motivo_form.is_valid():
            motivo = motivo_form.save(commit=False)
            if recibo is None:
                # Si no hay recibo existente, crea uno nuevo
                recibo = Recibo.objects.create(comunidad=comunidad)
            motivo.recibo = recibo
            motivo.save()
            # Redirigir al formulario de ese recibo para seguir editándolo
            return redirect('home:editar_recibo', recibo_id=recibo.id)
    else:
        motivo_form = MotivoReciboForm()
    
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    return render(request, 'home/crear_motivo.html', {'segment': 'gastos', 'motivo_form': motivo_form, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'recibo': recibo, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def editar_recibo(request, recibo_id):
    recibo = get_object_or_404(Recibo, pk=recibo_id)
    comunidad_id = recibo.comunidad_id
    motivos_recibo = Motivo.objects.filter(recibo=recibo)
    total_gastos = sum(motivo.cantidad for motivo in motivos_recibo)

    if recibo.archivo and request.GET.get('download') == 'true':
        with open(recibo.archivo.path, 'rb') as file:
            contenido = file.read()
        tipo_contenido, _ = mimetypes.guess_type(recibo.archivo.path)
        response = HttpResponse(contenido, content_type=tipo_contenido)
        response['Content-Disposition'] = f'attachment; filename="{recibo.archivo.name}"'
        return response
    
    if request.method == 'POST':
        recibo_form = ReciboForm(request.POST, instance=recibo)
        motivo_recibo_formset = MotivoReciboFormSet(request.POST, instance=recibo)
        

        if total_gastos != recibo.cantidad_total:
            return redirect('home:editar_recibo', recibo_id=recibo_id)
        
        else:
            
            eventos_calendario = Calendario.objects.filter(titulo=f"Recibo: {recibo.titulo}")
            for evento_calendario in eventos_calendario:
                evento_calendario.descripcion = recibo.descripcion
                evento_calendario.fecha = recibo.fecha_tope
                evento_calendario.save()

            return redirect('home:gastos', comunidad_seleccionada=comunidad_id) 
    else:
        recibo_form = ReciboForm(instance=recibo)
        motivo_recibo_formset = MotivoReciboFormSet(instance=recibo)
        motivo_recibo_formset = [form for form in motivo_recibo_formset.forms if form.instance.tipo and form.instance.cantidad]

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    return render(request, 'home/editar_recibo.html', {
        'segment': 'gastos',
        'recibo': recibo,
        'recibo_form': recibo_form,
        'motivo_recibo_formset': motivo_recibo_formset,
        'comunidad_id': comunidad_id,
        'chats_no_leidos': chats_no_leidos,
        'total_gastos': total_gastos,
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    })





@login_required(login_url="/login/login/")
def mostrar_modificar_gastos_recibos(request, comunidad_seleccionada):
    historial_completo = []

    # Obtener todos los gastos de la comunidad
    gastos_comunidad = Gasto.objects.filter(comunidad=comunidad_seleccionada)
    for gasto in gastos_comunidad:
        historial_completo.append({'tipo': 'Gasto', 'usuario': gasto.usuario.email, 'id': gasto.id, 'fecha_tope': gasto.fecha_tope, 'fecha': gasto.fecha, 'titulo': gasto.titulo, 'descripcion': gasto.descripcion, 'cantidad_total': gasto.cantidad_total, 'estado':gasto.estado})

    # Obtener todos los gastos personales del usuario
    gastos_personales = PagosUsuario.objects.filter(comunidad=comunidad_seleccionada)
    for gasto_personal in gastos_personales:
        historial_completo.append({'tipo': 'Gasto Personal', 'usuario': gasto_personal.usuario.email, 'id': gasto_personal.id, 'fecha': gasto_personal.fecha, 'titulo': gasto_personal.titulo, 'descripcion': gasto_personal.descripcion, 'cantidad_total': gasto_personal.cantidad, 'estado':gasto_personal.estado})


    # Obtener todos los recibos de una comunidad
    recibos = Recibo.objects.filter(comunidad=comunidad_seleccionada)
    for recibo in recibos:
        historial_completo.append({'tipo': 'Recibo', 'id': recibo.id, 'fecha_tope': recibo.fecha_tope, 'fecha': recibo.fecha, 'titulo': recibo.titulo, 'descripcion': recibo.descripcion, 'cantidad_total': recibo.cantidad_total, 'estado':''})


    # Ordenar el historial por fecha en orden descendente
    historial_completo.sort(key=lambda x: x['fecha'], reverse=True)

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    return render(request, 'home/modificar_gastos_recibos.html', {'segment': 'gastos', 'comunidad_seleccionada': comunidad_seleccionada, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'historial_completo': historial_completo, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def eliminar_recibo_gasto(request, comunidad_seleccionada, tipo, recibo_id):
    comunidad = get_object_or_404(Comunidad, pk=comunidad_seleccionada)

    if tipo == 'gasto':
        gasto = get_object_or_404(Gasto, pk=recibo_id, comunidad=comunidad)
        
        if not gasto.usuario:
            # Obtener los PagosUsuarios correspondientes al gasto
            pagos_usuarios = PagosUsuario.objects.filter(comunidad=comunidad, titulo=gasto.titulo, descripcion=gasto.descripcion, fecha=gasto.fecha_tope)
            
            # Eliminar los PagosUsuarios encontrados
            pagos_usuarios.delete()
            
            # Restaurar el dinero de la comunidad si el gasto fue pagado
            if gasto.estado == 'pagado':
                comunidad.dinero += gasto.cantidad_total
                comunidad.save()

        # Eliminar el evento del calenadrio
        Calendario.objects.filter(usuario=request.user, titulo=f"Gasto: {gasto.titulo}", descripcion=gasto.descripcion, fecha=gasto.fecha_tope).delete()

        # Eliminar el gasto
        gasto.delete()

    elif tipo == 'recibo':
        recibo = get_object_or_404(Recibo, pk=recibo_id, comunidad=comunidad)
        
        # Obtener los PagosUsuarios correspondientes al recibo
        pagos_usuarios = PagosUsuario.objects.filter(comunidad=comunidad, titulo=recibo.titulo, descripcion=recibo.descripcion, fecha=recibo.fecha_tope)
        
        # Eliminar los PagosUsuarios encontrados
        pagos_usuarios.delete()
        
        # Restaurar el dinero de la comunidad
        comunidad.dinero += recibo.cantidad_total
        comunidad.save()

        # Eliminar el evento del calenadrio
        Calendario.objects.filter(usuario=request.user, titulo=f"Recibo: {recibo.titulo}", descripcion=recibo.descripcion, fecha=recibo.fecha_tope).delete()

        # Eliminar el recibo
        recibo.delete()

    elif tipo == 'gasto_personal':
        gasto_personal = get_object_or_404(PagosUsuario, pk=recibo_id, comunidad=comunidad)
        
        # Eliminar el evento del calenadrio
        Calendario.objects.filter(usuario=gasto_personal.usuario, titulo=f"Gasto Personal: {gasto_personal.titulo}", descripcion=gasto_personal.descripcion, fecha=gasto_personal.fecha).delete()

        # Eliminar el gasto personal
        gasto_personal.delete()

    # Redirigir a la página de gastos
    return redirect('home:mostrar_modificar_gastos_recibos', comunidad_seleccionada=comunidad_seleccionada)



@login_required(login_url="/login/login/")
def editar_recibo_gasto(request, comunidad_seleccionada, tipo, recibo_id):
    comunidad = get_object_or_404(Comunidad, pk=comunidad_seleccionada)
    
    if tipo == 'gasto':
        recibo = get_object_or_404(Gasto, pk=recibo_id, comunidad=comunidad)
        form = GastoForm(request.POST or None, request.FILES or None, instance=recibo)
    elif tipo == 'recibo':
        recibo = get_object_or_404(Recibo, pk=recibo_id, comunidad=comunidad)
        form = ReciboForm(request.POST or None, request.FILES or None, instance=recibo)
    elif tipo == 'gasto_personal':
        recibo = get_object_or_404(PagosUsuario, pk=recibo_id, comunidad=comunidad)
        form = PagosUsuarioForm(request.POST or None, request.FILES or None, instance=recibo)
    
    if request.method == 'POST' and form.is_valid():
        edited_recibo = form.save(commit=False)
        
        # Obtain the amount paid from the form
        if tipo == 'gasto_personal':
            cantidad_pagada = form.cleaned_data.get('cantidad_pagada', 0)
            # Only update the user's balance if the paid amount is greater than expected
            if edited_recibo.cantidad < cantidad_pagada:
                extra_amount = cantidad_pagada - edited_recibo.cantidad
                usuario_pagador = UserProfile.objects.get(user=recibo.usuario)
                usuario_pagador.saldo += extra_amount
                usuario_pagador.save()
        else:
            cantidad_pagada = form.cleaned_data.get('cantidad_total', 0)
            # Only update the user's balance if the paid amount is greater than expected
            if edited_recibo.cantidad_total < cantidad_pagada:
                extra_amount = cantidad_pagada - edited_recibo.cantidad_total
                usuario_pagador = UserProfile.objects.get(user=recibo.usuario)
                usuario_pagador.saldo += extra_amount
                usuario_pagador.save()

        # Save changes to the recibo or gasto
        edited_recibo.save()
        
        # Update the calendar event
        try:
            evento_calendario = Calendario.objects.get(titulo=f"{tipo.capitalize()}: {edited_recibo.titulo}")
            evento_calendario.descripcion = edited_recibo.descripcion
            evento_calendario.fecha = edited_recibo.fecha_tope
            evento_calendario.save()
        except Calendario.DoesNotExist:
            pass
        
        # Check if the state has changed to "paid"
        if edited_recibo.estado == 'pagado':
            # Update the community's money
            if tipo in ['gasto', 'recibo']:
                comunidad.dinero += edited_recibo.cantidad_total
            elif tipo == 'gasto_personal':
                comunidad.dinero += edited_recibo.cantidad
            comunidad.save()
        
        return redirect('home:gastos')

    # Check if there is an attached file to download
    if recibo.archivo and request.GET.get('download') == 'true':
        with open(recibo.archivo.path, 'rb') as file:
            contenido = file.read()

        tipo_contenido, _ = mimetypes.guess_type(recibo.archivo.path)
        response = HttpResponse(contenido, content_type=tipo_contenido)
        response['Content-Disposition'] = f'attachment; filename="{recibo.archivo.name}"'

        return response

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    context = {
        'segment': 'gastos',
        'form': form,
        'comunidad_seleccionada': comunidad_seleccionada,
        'tipo': tipo,
        'recibo': recibo, 
        'chats_no_leidos': chats_no_leidos, 
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    }
    return render(request, 'home/editar_recibo_gasto.html', context)





# ---------------------------------------------------------- EDIT PROFILE ---------------------------------------------------------- 
@login_required(login_url="/login/login/")
def edit_profile(request):
    msg = None
    success = False
    user_instance = request.user
    profile_instance = user_instance.userprofile

    if request.method == "POST":
        # Manejar el formulario de perfil
        user_form = UpdateProfileForm(request.POST, instance=user_instance)
        profile_form = CrearUserProfileForm(request.POST, instance=profile_instance)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            success = True
        else:
            msg = '¡Formulario no válido!'
    else:
        user_form = UpdateProfileForm(instance=user_instance)
        profile_form = CrearUserProfileForm(instance=profile_instance)
    
    # Manejar la actualización de la imagen de perfil
    if request.method == "POST" and 'profile_img_submit' in request.POST:
        profile_IMG = UpdateIMGForm(request.POST, request.FILES, instance=profile_instance)
        
        if profile_IMG.is_valid():
            profile_instance.IMG_profile = profile_IMG.cleaned_data['IMG_profile']
            profile_instance.save()
            return redirect('home:config')
        else:
            msg = '¡Formulario de imagen no válido!'
    else:
        profile_IMG = UpdateIMGForm()

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    return render(request, "home/config.html", {'segment': 'config', "user_form": user_form, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, "profile_form" : profile_form, "profile_IMG": profile_IMG, "msg": msg, "success": success, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})





# ---------------------------------------------------------- EDITAR COMUNIDAD ---------------------------------------------------------- 
@login_required(login_url="/login/login/")
def comunidades_configuracion(request, comunidad_seleccionada=False):
    viviendas_usuario = Vivienda.objects.filter(usuario=request.user)
    comunidades = [vivienda.comunidad for vivienda in viviendas_usuario]
    comunidades_usuario = Comunidad.objects.filter(vivienda__usuario=request.user).distinct()
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if not comunidad_seleccionada:
        if comunidades:
            primera_comunidad = comunidades[0]
            return redirect('home:comunidades_configuracion', comunidad_seleccionada=primera_comunidad.pk)

    # Obtener la comunidad seleccionada
    comunidad_seleccionada = get_object_or_404(Comunidad, pk=comunidad_seleccionada)

    if request.method == 'POST':
        # Procesar el formulario para editar la comunidad
        form = EditarComunidadForm(request.POST, instance=comunidad_seleccionada)
        if form.is_valid():
            form.save()

        # Procesar el formulario para crear un nuevo anuncio
        crear_anuncio_form = CrearAnuncioForm(request.POST)
        if crear_anuncio_form.is_valid():
            titulo = crear_anuncio_form.cleaned_data['titulo']
            descripcion = crear_anuncio_form.cleaned_data['descripcion']
            fecha_anuncio = crear_anuncio_form.cleaned_data['fecha_anuncio']
            anuncio = Anuncio.objects.create(comunidad=comunidad_seleccionada, titulo=titulo, descripcion=descripcion, fecha_anuncio=fecha_anuncio)
            
            # Añadir el anuncio al calendario de todos los usuarios de la comunidad
            usuarios = Vivienda.objects.filter(comunidad=comunidad_seleccionada).values_list('usuario', flat=True).distinct()
            for usuario_id in usuarios:
                usuario = User.objects.get(id=usuario_id)
                Calendario.objects.create(
                    usuario=usuario,
                    titulo=f"Anuncio: {titulo}",
                    descripcion=descripcion,
                    fecha=fecha_anuncio
                )

        # Procesar el formulario para el seguro de la comunidad
        seguro_comunidad_instance = None
        if hasattr(comunidad_seleccionada, 'segurocomunidad'):
            seguro_comunidad_instance = comunidad_seleccionada.segurocomunidad
        seguro_comunidad_form = SeguroComunidadForm(request.POST, instance=seguro_comunidad_instance)
        if seguro_comunidad_form.is_valid():
            seguro_comunidad_form.save()

        if not comunidad_seleccionada:
            if comunidades:
                primera_comunidad = comunidades[0]
                return redirect('home:comunidades_configuracion', comunidad_seleccionada=primera_comunidad.pk)

        return redirect('home:comunidades_configuracion', comunidad_seleccionada=comunidad_seleccionada.pk)

    form = EditarComunidadForm(instance=comunidad_seleccionada)
    crear_anuncio_form = CrearAnuncioForm()
    seguro_comunidad_instance = None
    if hasattr(comunidad_seleccionada, 'segurocomunidad'):
        seguro_comunidad_instance = comunidad_seleccionada.segurocomunidad
    seguro_comunidad_form = SeguroComunidadForm(instance=seguro_comunidad_instance)

    usuarios = Vivienda.objects.filter(comunidad=comunidad_seleccionada).exclude(usuario=request.user).values_list('usuario', flat=True).distinct()

    return render(request, 'home/configuracion_comunidades.html', {
        'comunidades_usuario': comunidades_usuario,
        'comunidad_seleccionada': comunidad_seleccionada,
        'segment': 'communidad',
        'comunidades': comunidades,
        'form': form,
        'usuarios': usuarios,
        'crear_anuncio_form': crear_anuncio_form,
        'seguro_comunidad_form': seguro_comunidad_form,
        "chats_no_leidos": chats_no_leidos, 
        "num_mensajes_no_leidos": num_mensajes_no_leidos, 
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    })



@login_required(login_url="/login/login/")
def administrar_viviendas(request, comunidad_seleccionada):
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()
    comunidad = get_object_or_404(Comunidad, id=comunidad_seleccionada)
    viviendas = Vivienda.objects.filter(comunidad=comunidad)

    return render(request, 'home/administrar_viviendas.html', {
        'segment': 'communidad',
        'comunidad': comunidad,
        'viviendas': viviendas,
        "chats_no_leidos": chats_no_leidos, 
        "num_mensajes_no_leidos": num_mensajes_no_leidos,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    })

@login_required(login_url="/login/login/")
def eliminar_vivienda(request, comunidad_id, viviendas_id):
    vivienda = get_object_or_404(Vivienda, id=viviendas_id)
    if request.method == 'POST':
        vivienda.delete()
        return redirect('home:administrar_viviendas', comunidad_seleccionada=comunidad_id)
    return redirect('home:administrar_viviendas', comunidad_seleccionada=comunidad_id)


@login_required(login_url="/login/login/")
def asignar_usuario_comunidad(request, comunidad_id):
    comunidad = Comunidad.objects.get(pk=comunidad_id)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if request.method == 'POST':
        form = AsignarUsuarioComunidadForm(request.POST)
        if form.is_valid():
            vivienda = form.save(commit=False)
            vivienda.comunidad = comunidad
            vivienda.save()
            return redirect('home:administrar_viviendas', comunidad_seleccionada=comunidad_id)
    else:
        form = AsignarUsuarioComunidadForm()

    return render(request, 'home/añadir_usuario_comunidad.html', {'segment': 'communidad', 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, "chats_no_leidos": chats_no_leidos, "num_mensajes_no_leidos": num_mensajes_no_leidos, 'form': form, 'comunidad': comunidad})


@login_required(login_url="/login/login/")
def editar_vivienda_comunidad(request, comunidad_id, viviendas_id):
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()
    msg = None
    success = False
    vivienda = get_object_or_404(Vivienda, id=viviendas_id)

    if request.method == "POST":
        viviendas_form = AsignarUsuarioComunidadForm(request.POST, instance=vivienda)
        
        if viviendas_form.is_valid():
            viviendas_form.save()
            success = True
            usuario_vivienda = vivienda.usuario

            if vivienda.rol_comunidad == 'community_president' or vivienda.rol_comunidad == 'community_vicepresident':
                if usuario_vivienda.userprofile.user_rol != 'lume':
                    usuario_vivienda.userprofile.user_rol = 'community_admin'
                    usuario_vivienda.userprofile.save()

            elif vivienda.rol_comunidad == 'community_user':
                if usuario_vivienda.userprofile.user_rol != 'lume':
                    usuario_vivienda.userprofile.user_rol = 'community_user'
                    usuario_vivienda.userprofile.save()

        else:
            msg = '¡Formulario no válido!'

    else:
        viviendas_form = AsignarUsuarioComunidadForm(instance=vivienda)

    return render(request, "home/editar_vivienda.html", {'segment': 'communidad', "chats_no_leidos": chats_no_leidos, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, "num_mensajes_no_leidos": num_mensajes_no_leidos, "comunidad_id": comunidad_id, "viviendas_form": viviendas_form, "msg": msg, "success": success})


@login_required(login_url="/login/login/")
def administrar_distribucion_gastos(request, comunidad_id):
    comunidad = get_object_or_404(Comunidad, id=comunidad_id)
    viviendas = Vivienda.objects.filter(comunidad=comunidad)
    success = False
    msg = None
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if request.method == 'POST':
        metodo_pago_form = MetodoPagoForm(request.POST, instance=comunidad)
        porcentaje_forms = [PorcentajePagoForm(request.POST, prefix=str(vivienda.id), instance=vivienda) for vivienda in viviendas]
        
        if metodo_pago_form.is_valid():
            metodo_pago_form.save()
            valid_forms = all([form.is_valid() for form in porcentaje_forms])
            
            if valid_forms:

                if comunidad.metodo_pago == 'porcentajes':

                    total_porcentaje = sum([form.cleaned_data.get('porcentaje_pago', 0) for form in porcentaje_forms])

                    if total_porcentaje == 100:
                        for form in porcentaje_forms:
                            form.save()
                        
                        if comunidad.metodo_pago == 'igual':
                            for vivienda in viviendas:
                                vivienda.porcentaje_pago = 0.00
                                vivienda.save()

                        success = True
                    else:
                        msg = "El porcentaje total asignado debe ser igual a 100."

            else:

                for vivienda in viviendas:
                    vivienda.porcentaje_pago = 0.00
                    vivienda.save()
                
                success = True

    else:
        metodo_pago_form = MetodoPagoForm(instance=comunidad)
        porcentaje_forms = [PorcentajePagoForm(prefix=str(vivienda.id), instance=vivienda) for vivienda in viviendas]

    return render(request, 'home/administrar_distribucion_gastos.html', {
        'segment': 'communidad',
        'comunidad': comunidad,
        'metodo_pago_form': metodo_pago_form,
        'porcentaje_forms': porcentaje_forms,
        'msg': msg,
        'success': success,
        'chats_no_leidos': chats_no_leidos,
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'num_notificaciones_no_leidas': num_notificaciones_no_leidas,
    })




# ---------------------------------------------------------- EDITAR EMPRESA ---------------------------------------------------------- 
@login_required(login_url="/login/login/")
def edit_empresa_profile(request):
    empresa = Empresa.objects.filter(trabajador__usuario=request.user).first()
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    notificaciones_no_leidas = Notificacion.objects.filter(user=request.user, leida=False)
    num_notificaciones_no_leidas = notificaciones_no_leidas.count()

    if request.method == 'POST':
        form_empresa = EditarEmpresaForm(request.POST, instance=empresa)
        if form_empresa.is_valid():
            form_empresa.save()
            return redirect('home/config_empresa')
        
        form_imagen = UpdateIMGEmpresaForm(request.POST, request.FILES, instance=empresa)

        if form_imagen.is_valid():
            form_imagen.save()
            return redirect('home/config_empresa')

        if 'trabajador_id' in request.POST:
            trabajador_id = request.POST.get('trabajador_id')
            trabajador = Trabajador.objects.get(pk=trabajador_id)
            trabajador.delete()
            return redirect('home/config_empresa')
    else:
        form_empresa = EditarEmpresaForm(instance=empresa)
        form_imagen = UpdateIMGEmpresaForm(instance=empresa)

    trabajadores = Trabajador.objects.filter(empresa=empresa)

    return render(request, 'home/config_empresa.html', {'segment': 'empresa', 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos': num_mensajes_no_leidos, 'notificaciones_no_leidas': notificaciones_no_leidas, 'num_notificaciones_no_leidas': num_notificaciones_no_leidas, 'form_empresa': form_empresa, 'form_imagen': form_imagen, 'empresa': empresa, 'trabajadores': trabajadores})
