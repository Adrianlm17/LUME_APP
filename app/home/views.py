import calendar
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import TemplateDoesNotExist, loader
from django.urls import reverse
from app.admin_lume.forms import CrearUserProfileForm
from app.home.forms import ActaForm, ChatForm, ExtendsChatForm, GastoForm, MotivoReciboForm, MotivoReciboFormSet, NotaForm, ReciboForm, UpdateProfileForm
from app.home.models import Nota, User
from django.db.models import Q, F
from .models import Acta, Anuncio, Calendario, Chat, ChatReadBy, Comunidad, ExtendsChat, Gasto, Motivo, Nota, PagosUsuario, Recibo, Transaccion, UserProfile, Vivienda  



@login_required(login_url="/login/login/")
def home_index(request):
    hoy = datetime.now()
    fecha_limite = hoy + timedelta(days=15)
    proximos_eventos = Calendario.objects.filter(usuario=request.user, fecha__range=[hoy, fecha_limite]).order_by('fecha')
    notas = Nota.objects.filter(usuario=request.user)
    viviendas_usuario = Vivienda.objects.filter(usuario=request.user)
    comunidades_usuario = [vivienda.comunidad for vivienda in viviendas_usuario]
    anuncios = Anuncio.objects.filter(comunidad__in=comunidades_usuario)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()

    admin = False

    if hasattr(request.user, 'userprofile'):
        admin = request.user.userprofile.user_rol if request.user.userprofile.user_rol == 'lume' else False

    usuario_comunidad = False

    usuario_comunidad = Vivienda.objects.filter(usuario=request.user).exists()

    context = {
        'segment': 'index',
        'notas': notas,
        'proximos_eventos': proximos_eventos,
        'anuncios': anuncios,
        'chats_no_leidos': chats_no_leidos,
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
        'admin': admin,
        'usuario_comunidad': usuario_comunidad,
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
    anuncios = Anuncio.objects.filter(comunidad__in=comunidades_usuario)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()

    return render(request, 'home/index.html', {'notas': notas, 'segment': 'index', 'proximos_eventos': proximos_eventos, 'anuncios': anuncios, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})



def detalles_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Anuncio, id=anuncio_id)
    context = {
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

    return render(request, 'home/notas.html', {'segment': 'index', 'nota_form': nota_form, "msg": msg, "success": success})


def edit_nota(request, nota_id):
    msg = None
    success = False
    notas = get_object_or_404(Nota, id=nota_id)

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

    return render(request, 'home/edit_nota.html', {'segment': 'index', 'nota_form': nota_form, "msg": msg, "success": success})


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
    anuncios = Anuncio.objects.filter(comunidad__in=comunidades_usuario)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()

    context = {
        'segment': 'index',
        'notas': notas_usuario,
        'proximos_eventos': proximos_eventos,
        'anuncios': anuncios, 
        'chats_no_leidos': chats_no_leidos,
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
    }

    return render(request, 'home/index.html', context)





# ---------------------------------------------------------- CHAT ---------------------------------------------------------- 
@login_required(login_url="/login/login/")
def chat(request):
    user_chats = Chat.objects.filter(Q(user=request.user) | Q(mensaje_user=request.user))
    users = User.objects.exclude(id=request.user.id)
    
    user_read_chats = ChatReadBy.objects.filter(user=request.user, is_read=True).values_list('chat__id', flat=True)

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()
    
    return render(request, 'home/chat.html', {'segment': 'chat', 'user_chats': user_chats, 'users': users, 'user_read_chats': user_read_chats, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def open_chat(request):
    if request.method == 'POST':
        user_id = request.POST.get('usuario')
        recipient = get_object_or_404(User, id=user_id)
        chat, created = Chat.objects.get_or_create(user=request.user, mensaje_user=recipient)
        chat_read_by, created = ChatReadBy.objects.get_or_create(chat=chat, user=request.user)
        
        
        if created:  
            chat_read_by.is_read = True
            chat_read_by.save()
        
        else:
            chat_read_by = ChatReadBy.objects.get(chat=chat, user=request.user)
            chat_read_by.is_read = True
            chat_read_by.save()

        return redirect('home:chat_detail', chat_id=chat.id)
    return redirect('home:chat')




@login_required(login_url="/login/login/")
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
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
                return redirect('home:chat_detail', chat_id=chat.id)
        else:

            form = ExtendsChatForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.chat = chat
                message.user_send = request.user
                message.save()
                chat.last_chat = message.text
                chat.save()

                if chat.user == request.user:
                    recipient = chat.mensaje_user
                else:
                    recipient = chat.user
                
                chat_read_by, created = ChatReadBy.objects.get_or_create(chat=chat, user=recipient)
                chat_read_by.is_read = False
                chat_read_by.save()

                return redirect('home:chat_detail', chat_id=chat.id)
    else:
        title_form = ChatForm(instance=chat)

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()

    return render(request, 'home/chat_detail.html', {'segment': 'chat', 'chat': chat, 'messages': messages, 'form': form, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos, 'title_form': title_form})


    



# ---------------------------------------------------------- ACTAS ---------------------------------------------------------- 
@login_required(login_url="/login/login/")
def actas(request):
    viviendas = Vivienda.objects.filter(usuario=request.user)
    comunidades_usuario = [vivienda.comunidad for vivienda in viviendas]
    actas_usuario = Acta.objects.filter(comunidad__in=comunidades_usuario)

    es_presidente_o_vicepresidente = any(
        vivienda.rol_comunidad in ['community_president', 'community_vicepresident'] for vivienda in viviendas
    )

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()

    return render(request, 'home/actas.html', {'segment': 'actas', 'actas_usuario': actas_usuario, 'es_presidente_o_vicepresidente': es_presidente_o_vicepresidente, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})



@login_required(login_url="/login/login/")
def crear_acta(request):
    if request.method == 'POST':
        acta_form = ActaForm(request.POST, user=request.user)
        if acta_form.is_valid():
            acta = acta_form.save(commit=False)
            acta.firmada = request.user
            acta.fecha = timezone.now()
            acta.save()
            return redirect('home:actas')
    else:
        acta_form = ActaForm(user=request.user)

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()

    return render(request, 'home/crear_acta.html', {'segment': 'actas', 'acta_form': acta_form, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def ver_acta(request, acta_id):
    acta = get_object_or_404(Acta, id=acta_id)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()

    return render(request, 'home/ver_acta.html', {'segment': 'actas', 'acta': acta, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})






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

    titulo = f"{meses_espanol[mes].capitalize()} | {año}"
    eventos_mes_actual = Calendario.objects.filter(fecha__year=año, fecha__month=mes)
    
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

    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()

    return render(request, 'home/calendario.html', {
        'segment': 'calendario',
        'titulo': titulo,
        'calendario_mes': calendario_mes,
        'dias_de_la_semana': calendar.day_name,
        'url_mes_anterior': url_mes_anterior,
        'url_mes_siguiente': url_mes_siguiente, 
        'chats_no_leidos': chats_no_leidos, 
        'num_mensajes_no_leidos':num_mensajes_no_leidos
    })


@login_required(login_url="/login/login/")
def crear_recordatorio(request):
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()

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
        return render(request, 'home/crear_recordatorio.html', {'segment': 'calendario', 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def detalle_evento(request, evento_id):
    evento = get_object_or_404(Calendario, id=evento_id)
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()

    if request.method == 'POST':
        evento.titulo = request.POST.get('titulo')
        evento.descripcion = request.POST.get('descripcion')
        evento.save()
        return redirect('home:detalle_evento', evento_id=evento.id)
    
    return render(request, 'home/detalle_evento.html', {'segment': 'calendario', 'evento': evento, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


@login_required(login_url="/login/login/")
def delete_calendario(request, recordatorio_id):
    recordatorio_form = get_object_or_404(Calendario, id=recordatorio_id)

    if request.method == 'POST':
        recordatorio_form.delete()

    hoy = datetime.now()
    año = hoy.year
    mes = hoy.month

    return redirect('home:calendario', año=año, mes=mes)






# ---------------------------------------------------------- GASTOS ---------------------------------------------------------- 
@login_required(login_url="/login/login/")
def gastos(request, comunidad_seleccionada=False):
    user_profile = UserProfile.objects.get(user=request.user)
    viviendas_usuario = Vivienda.objects.filter(usuario=request.user)
    comunidades = [vivienda.comunidad for vivienda in viviendas_usuario]

    es_presidente_o_vicepresidente = False

    if not comunidad_seleccionada:
        if comunidades:
            primera_comunidad = comunidades[0]
            return redirect('home:gastos', comunidad_seleccionada=primera_comunidad.pk)
    else:
        es_presidente_o_vicepresidente = Vivienda.objects.filter(usuario=request.user, comunidad=comunidad_seleccionada, rol_comunidad__in=['community_president', 'community_vicepresident']).exists()

        # Obtener la comunidad seleccionada
        comunidad_seleccionada = Comunidad.objects.get(pk=comunidad_seleccionada)

        # Obtener el último movimiento de la comunidad
        ultimo_movimiento = obtener_ultimo_movimiento(comunidad_seleccionada)

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

        return render(request, 'home/gastos.html', {'segment': 'gastos', 'user_profile': user_profile, 'comunidades': comunidades, 'comunidad_seleccionada': comunidad_seleccionada, 'ultimo_movimiento': ultimo_movimiento, 'dinero_actual_comunidad': dinero_actual_comunidad, 'proximo_recibo_pendiente': proximo_recibo_pendiente, 'historial_dinero_mensual_comunidad': historial_dinero_mensual_comunidad, 'historial_dinero_comunidad': historial_dinero_comunidad, 'distribucion_gastos_ultimo_recibo': distribucion_gastos_ultimo_recibo, 'proximos_pagos': proximos_pagos, 'mis_pagos': mis_pagos, 'es_presidente_o_vicepresidente': es_presidente_o_vicepresidente})


def obtener_historial_mensual_dinero_comunidad(comunidad):
    historial = []

    # Obtener todos los recibos de la comunidad para el año actual
    recibos = Recibo.objects.filter(comunidad=comunidad, fecha_tope__year=timezone.now().year)
    
    # Iterar sobre cada recibo para obtener la información relevante
    for recibo in recibos:
        historial.append({
            'tipo': 'Recibo',
            'titulo': recibo.titulo,
            'fecha': recibo.fecha_tope,
            'cantidad': recibo.cantidad_total
        })
    
    return historial


def obtener_historial_dinero_comunidad(comunidad, usuario):
    historial = []

    # Obtener todos los gastos de la comunidad para el año actual
    gastos_comunidad = Gasto.objects.filter(comunidad=comunidad, fecha_tope__year=timezone.now().year, usuario=None).order_by('-id')[:2]
    
    # Iterar sobre cada gasto de la comunidad
    for gasto in gastos_comunidad:
        historial.append({
            'tipo': 'Gasto Comunidad',
            'titulo': gasto.titulo,
            'fecha': gasto.fecha_tope,
            'cantidad': gasto.cantidad_total,
            'estado': gasto.estado
        })

    # Obtener todos los gastos personales del usuario para el año actual
    gastos_personales = PagosUsuario.objects.filter(usuario=usuario).order_by('-id')[:2]
    
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


def obtener_ultimo_movimiento(comunidad):
    try:
        ultimo_gasto = Gasto.objects.filter(comunidad=comunidad).latest('fecha_tope')
        ultimo_transaccion = Transaccion.objects.filter(comunidad=comunidad).latest('fecha')

        if ultimo_gasto.fecha > ultimo_transaccion.fecha:
            return f"Gasto: ${ultimo_gasto.cantidad_total} - {ultimo_gasto.fecha}"
        else:
            return f"Transacción: ${ultimo_transaccion.monto} - {ultimo_transaccion.fecha}"
    except:
        return "No hay movimientos"


def obtener_proximo_recibo_pendiente(comunidad):
    try:
        ultimo_recibo = Recibo.objects.filter(comunidad=comunidad).latest('fecha_tope')
        return ultimo_recibo.fecha_tope.strftime("%Y-%m-%d")
    except:
        return "No hay recibo pendiente"



def obtener_distribucion_gastos_ultimo_recibo(comunidad):
    try:
        # Obtener el último recibo
        ultimo_recibo = Recibo.objects.filter(comunidad=comunidad).latest('fecha_tope')
        
        # Obtener todos los tipos de gastos posibles
        tipos_gastos = ['luz', 'agua', 'gas', 'piscina', 'jardineria', 'personal', 'limpieza', 'extras']
        
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
    # Obtener la comunidad
    comunidad = Comunidad.objects.get(pk=comunidad_id)
    
    # Obtener el historial completo de la comunidad
    historial_completo = obtener_historial_completo(comunidad, request.user)

    return render(request, 'home/historial_completo.html', {'segment': 'gastos', 'comunidad': comunidad, 'historial_completo': historial_completo})


@login_required(login_url="/login/login/")
def ver_historial_individual(request, tipo, movimiento_id):
    if tipo == 'gasto':
        movimiento = get_object_or_404(Gasto, pk=movimiento_id)
    elif tipo == 'gasto_personal':
        movimiento = get_object_or_404(PagosUsuario, pk=movimiento_id)
    else:
        pass
    return render(request, 'home/ver_historial_individual.html', {'segment': 'gastos', 'movimiento': movimiento})


@login_required(login_url="/login/login/")
def cambiar_comunidad(request, comunidad_id):
    if request.method == 'POST':
        nueva_comunidad_id = request.POST.get('comunidad_id')
        request.session['comunidad_id'] = nueva_comunidad_id
        return redirect('home:gastos', comunidad_seleccionada=nueva_comunidad_id)
    else:
        return redirect(reverse('home:gastos'))



@login_required(login_url="/login/login/")
def crear_gasto(request, comunidad_seleccionada):
    comunidad = Comunidad.objects.get(pk=comunidad_seleccionada)
    
    if request.method == 'POST':
        gasto_form = GastoForm(request.POST)
        
        if gasto_form.is_valid():
            gasto = gasto_form.save(commit=False)
            gasto.comunidad = comunidad
            gasto.save()

            # Obtener el usuario asignado si tiene
            usuario = request.POST.get('usuario')
            
            if usuario:
                gasto.usuario = request.user
                gasto.save()
                
            else:
                # Calcular la cantidad que cada miembro de la comunidad debe pagar
                total_gasto = gasto.cantidad_total
                viviendas_comunidad = Vivienda.objects.filter(comunidad=comunidad)
                numero_viviendas = viviendas_comunidad.count()
                cantidad_por_vivienda = total_gasto / numero_viviendas

                # Crear un registro de pago para cada usuario de cada vivienda en la comunidad
                for vivienda in viviendas_comunidad:
                    pago = PagosUsuario.objects.create(
                        usuario=vivienda.usuario,
                        comunidad=comunidad,
                        titulo=gasto.titulo,
                        descripcion=gasto.descripcion,
                        fecha=gasto.fecha_tope,
                        cantidad=cantidad_por_vivienda,
                        estado='pendiente'
                    )

                comunidad.dinero_actual -= total_gasto
                comunidad.save()

                Transaccion.objects.create(
                    comunidad=comunidad,
                    monto=-total_gasto,
                    descripcion=f"Gasto: {gasto.titulo}"
                )

            return redirect('home:gastos')
    else:
        gasto_form = GastoForm()

    return render(request, 'home/crear_gasto.html', {
        'segment': 'gastos',
        'gasto_form': gasto_form,
        'comunidad': comunidad,
    })



@login_required(login_url="/login/login/")
def crear_recibo(request, comunidad_seleccionada):
    comunidad = Comunidad.objects.get(pk=comunidad_seleccionada)

    if request.method == 'POST':
        recibo_form = ReciboForm(request.POST)
        motivo_recibo_formset = MotivoReciboFormSet(request.POST)

        if recibo_form.is_valid() and motivo_recibo_formset.is_valid():
            recibo = recibo_form.save(commit=False)
            recibo.comunidad = comunidad
            recibo.save()

            # Calcular la cantidad que cada miembro de la comunidad debe pagar
            total_recibo = recibo.cantidad_total
            viviendas_comunidad = Vivienda.objects.filter(comunidad=comunidad)
            numero_viviendas = viviendas_comunidad.count()
            cantidad_por_usuario = total_recibo / numero_viviendas

            # Crear un registro de pago para cada usuario de cada vivienda en la comunidad
            for vivienda in viviendas_comunidad:
                pago = PagosUsuario.objects.create(
                    usuario=vivienda.usuario,
                    comunidad=comunidad,
                    titulo=recibo.titulo,
                    descripcion=recibo.descripcion,
                    fecha=recibo.fecha_tope,
                    cantidad=cantidad_por_usuario,
                    estado='pendiente'
                )

            # Restar el monto del recibo al dinero actual de la comunidad
            comunidad.dinero -= total_recibo
            comunidad.save()

            # Registrar la transacción en el modelo Transaccion
            Transaccion.objects.create(
                comunidad=comunidad,
                monto=-total_recibo,
                descripcion=f"Recibo: {recibo.titulo}"
            )

            # Después de guardar el recibo y los pagos, redirigir a gastos
            return redirect('home:crear_motivo', comunidad_seleccionada=comunidad_seleccionada)

    else:
        recibo_form = ReciboForm()
        motivo_recibo_formset = MotivoReciboFormSet()

    motivos_recibo = Recibo.objects.filter(comunidad=comunidad).order_by('-id').first().motivos.all() if Recibo.objects.filter(comunidad=comunidad) else None

    return render(request, 'home/crear_recibo.html', {
        'segment': 'gastos',
        'recibo_form': recibo_form,
        'motivo_recibo_formset': motivo_recibo_formset,
        'comunidad': comunidad,
        'motivos_recibo': motivos_recibo,
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
    return render(request, 'home/crear_motivo.html', {'segment': 'gastos', 'motivo_form': motivo_form, 'recibo': recibo})


@login_required(login_url="/login/login/")
def editar_recibo(request, recibo_id):
    recibo = get_object_or_404(Recibo, pk=recibo_id)
    comunidad_id = recibo.comunidad_id
    if request.method == 'POST':
        recibo_form = ReciboForm(request.POST, instance=recibo)
        motivo_recibo_formset = MotivoReciboFormSet(request.POST, instance=recibo)
        if recibo_form.is_valid() and motivo_recibo_formset.is_valid():
            recibo_form.save()
            motivo_recibo_formset.save()
            return redirect('home:gastos', comunidad_seleccionada=comunidad_id) 
    else:
        recibo_form = ReciboForm(instance=recibo)
        motivo_recibo_formset = MotivoReciboFormSet(instance=recibo)
    return render(request, 'home/editar_recibo.html', {'segment': 'gastos', 'recibo': recibo, 'recibo_form': recibo_form, 'motivo_recibo_formset': motivo_recibo_formset, 'comunidad_id': comunidad_id})


@login_required(login_url="/login/login/")
def mostrar_modificar_gastos_recibos(request, comunidad_seleccionada):
    historial_completo = []

    # Obtener todos los gastos de la comunidad
    gastos_comunidad = Gasto.objects.filter(comunidad=comunidad_seleccionada)
    for gasto in gastos_comunidad:
        historial_completo.append({'tipo': 'Gasto', 'id': gasto.id, 'fecha': gasto.fecha_tope, 'titulo': gasto.titulo, 'descripcion': gasto.descripcion, 'cantidad_total': gasto.cantidad_total, 'estado':gasto.estado})

    # Obtener todos los gastos personales del usuario
    gastos_personales = PagosUsuario.objects.filter(comunidad=comunidad_seleccionada)
    for gasto_personal in gastos_personales:
        historial_completo.append({'tipo': 'Gasto Personal', 'id': gasto_personal.id, 'fecha': gasto_personal.fecha, 'titulo': gasto_personal.titulo, 'descripcion': gasto_personal.descripcion, 'cantidad_total': gasto_personal.cantidad, 'estado':gasto_personal.estado})


    # Obtener todos los recibos de una comunidad
    recibos = Recibo.objects.filter(comunidad=comunidad_seleccionada)
    for recibo in recibos:
        historial_completo.append({'tipo': 'Recibo', 'id': recibo.id, 'fecha': recibo.fecha_tope, 'titulo': recibo.titulo, 'descripcion': recibo.descripcion, 'cantidad_total': recibo.cantidad_total, 'estado':''})


    # Ordenar el historial por fecha en orden descendente
    historial_completo.sort(key=lambda x: x['fecha'], reverse=True)

    
    return render(request, 'home/modificar_gastos_recibos.html', {'segment': 'gastos', 'comunidad_seleccionada': comunidad_seleccionada, 'historial_completo': historial_completo})


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

        # Eliminar el recibo
        recibo.delete()

    elif tipo == 'gasto_personal':
        gasto_personal = get_object_or_404(PagosUsuario, pk=recibo_id, comunidad=comunidad)
        
        # Eliminar el gasto personal
        gasto_personal.delete()

    # Redirigir a la página de gastos
    return redirect('home:gastos')



@login_required(login_url="/login/login/")
def editar_recibo_gasto(request, comunidad_seleccionada, tipo, recibo_id):
    comunidad = get_object_or_404(Comunidad, pk=comunidad_seleccionada)
    recibo = None
    pagos_usuarios = None
    form = None
    
    if tipo == 'gasto':
        gasto = get_object_or_404(Gasto, pk=recibo_id, comunidad=comunidad)
        form = GastoForm(instance=gasto)
    elif tipo == 'recibo':
        recibo = get_object_or_404(Recibo, pk=recibo_id, comunidad=comunidad)
        form = ReciboForm(instance=recibo)
    elif tipo == 'gasto_personal':
        recibo = get_object_or_404(PagosUsuario, pk=recibo_id, comunidad=comunidad)
        form = PagosUsuario()

    if request.method == 'POST':
        if tipo == 'gasto':
            form = GastoForm(request.POST, instance=gasto)
        elif tipo == 'recibo':
            form = ReciboForm(request.POST, instance=recibo)
        elif tipo == 'gasto_personal':
            form = GastoForm(request.POST, instance=recibo)
            
        
        if form.is_valid():
            edited_recibo = form.save(commit=False)
            edited_recibo.save()

            # Actualizar el dinero de la comunidad si se modifica la cantidad de un recibo o gasto
            if not edited_recibo.usuario:
                diferencia_cantidad = edited_recibo.cantidad_previa - edited_recibo.cantidad
                
                if tipo == 'gasto':
                    pagos_usuarios = PagosUsuario.objects.filter(comunidad=comunidad, titulo=gasto.titulo, descripcion=gasto.descripcion, fecha=gasto.fecha_tope)
                    pagos_usuarios.update(cantidad=F('cantidad') + diferencia_cantidad)
                elif tipo == 'recibo':
                    pagos_usuarios = PagosUsuario.objects.filter(comunidad=comunidad, titulo=recibo.titulo, descripcion=recibo.descripcion, fecha=recibo.fecha_tope)
                    pagos_usuarios.update(cantidad=F('cantidad') + diferencia_cantidad)
                elif tipo == 'gasto_personal':
                    pagos_usuarios = PagosUsuario.objects.filter(comunidad=comunidad, titulo=recibo.titulo, descripcion=recibo.descripcion, fecha=recibo.fecha_tope)
                    pagos_usuarios.update(cantidad=F('cantidad') + diferencia_cantidad)

                comunidad.dinero += diferencia_cantidad
                comunidad.save()

            return redirect('home:gastos')
    
    context = {
        'segment': 'gastos',
        'form': form,
        'comunidad_seleccionada': comunidad_seleccionada,
        'tipo': tipo,
        'recibo': recibo,
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
    
    chats_no_leidos = ChatReadBy.objects.filter(user=request.user, is_read=False)
    num_mensajes_no_leidos = chats_no_leidos.count()

    return render(request, "home/config.html", {'segment': 'config', "user_form": user_form, "profile_form" : profile_form, "msg": msg, "success": success, 'chats_no_leidos': chats_no_leidos, 'num_mensajes_no_leidos':num_mensajes_no_leidos})


