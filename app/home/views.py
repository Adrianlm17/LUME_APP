import calendar
from django.db.models import Sum
from datetime import datetime, timedelta
from django.forms import inlineformset_factory
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import TemplateDoesNotExist, loader
from django.urls import reverse
from app.admin_lume.forms import CrearUserProfileForm
from app.home.forms import ActaForm, ChatForm, ExtendsChatForm, GastoForm, MotivoReciboFormSet, NotaForm, ReciboForm, UpdateProfileForm
from app.home.models import Nota, User
from django.db.models import Q
from .models import Acta, Anuncio, Calendario, Chat, ChatReadBy, Comunidad, ExtendsChat, Gasto, Historial, Motivo, Nota, PagosHechos, ProximosPagos, Recibo, Transaccion, UltimosMovimientos, UserProfile, Vivienda  



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

    context = {
        'segment': 'index',
        'notas': notas,
        'proximos_eventos': proximos_eventos,
        'anuncios': anuncios,
        'chats_no_leidos': chats_no_leidos,
        'num_mensajes_no_leidos': num_mensajes_no_leidos,
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
def gastos(request, comunidad_seleccionada):
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
        historial_dinero_comunidad = obtener_historial_dinero_comunidad(comunidad_seleccionada)

        # Obtener la distribución de gastos del último recibo
        distribucion_gastos_ultimo_recibo = obtener_distribucion_gastos_ultimo_recibo(comunidad_seleccionada)

        # Obtener los últimos 10 pagos/derramas o recibos realizados
        ultimos_pagos_derramas_recibos = obtener_ultimos_pagos_derramas_recibos(comunidad_seleccionada)

        # Obtener los próximos pagos
        proximos_pagos = obtener_proximos_pagos(comunidad_seleccionada)

        # Obtener mis pagos
        mis_pagos = obtener_mis_pagos(request.user, comunidad_seleccionada)

        return render(request, 'home/gastos.html', {'user_profile': user_profile, 'comunidades': comunidades, 'comunidad_seleccionada': comunidad_seleccionada, 'ultimo_movimiento': ultimo_movimiento, 'dinero_actual_comunidad': dinero_actual_comunidad, 'proximo_recibo_pendiente': proximo_recibo_pendiente, 'historial_dinero_comunidad': historial_dinero_comunidad, 'distribucion_gastos_ultimo_recibo': distribucion_gastos_ultimo_recibo, 'ultimos_pagos_derramas_recibos': ultimos_pagos_derramas_recibos, 'proximos_pagos': proximos_pagos, 'mis_pagos': mis_pagos, 'es_presidente_o_vicepresidente': es_presidente_o_vicepresidente})


def obtener_ultimo_movimiento(comunidad):
    try:
        ultimo_gasto = Gasto.objects.filter(comunidad=comunidad).latest('fecha_tope')
        ultimo_transaccion = Transaccion.objects.filter(comunidad=comunidad).latest('fecha')

        if ultimo_gasto.fecha > ultimo_transaccion.fecha:
            return f"Gasto: ${ultimo_gasto.monto} - {ultimo_gasto.fecha}"
        else:
            return f"Transacción: ${ultimo_transaccion.monto} - {ultimo_transaccion.fecha}"
    except:
        return "No hay movimientos"


def obtener_proximo_recibo_pendiente(comunidad):
    try:
        proximo_recibo = Recibo.objects.filter(comunidad=comunidad, fecha_tope__gte=datetime.now()).order_by('fecha_tope').first()

        if proximo_recibo:
            if proximo_recibo.fecha_tope == datetime.now().date():
                return "HOY"
            else:
                return proximo_recibo.fecha_tope.strftime("%Y-%m-%d")
        else:
            return "Pendiente actualizar"
        
    except:
        return "Pendiente actualizar"

def obtener_historial_dinero_comunidad(comunidad):
    historial = []
    
    try:
        recibos = Recibo.objects.filter(comunidad=comunidad)

        for recibo in recibos:
            cantidad_total_a_pagar = recibo.cantidad_total * comunidad.numero_propietarios
            historial.append(Historial.objects.create(cantidad=cantidad_total_a_pagar, mes=recibo.fecha_tope.strftime("%Y-%m")))

        return historial
    except:
        return historial
    

def obtener_distribucion_gastos_ultimo_recibo(comunidad):
    try:
        ultimo_recibo = Recibo.objects.filter(comunidad=comunidad).latest('fecha_tope')
        motivos_recibo = Motivo.objects.filter(recibo=ultimo_recibo)

        distribucion = {}
        for motivo in motivos_recibo:
            distribucion[motivo.tipo] = motivo.cantidad

        return distribucion
    except:
        return {}


def obtener_ultimos_pagos_derramas_recibos(comunidad):
    return Recibo.objects.filter(comunidad=comunidad).order_by('-fecha_tope')[:10]


def obtener_proximos_pagos(comunidad):
    try:
        return Recibo.objects.filter(comunidad=comunidad, fecha__gte=datetime.now()).order_by('fecha')
    
    except:
        return []


def obtener_mis_pagos(usuario, comunidad):
    try:
        return Recibo.objects.filter(comunidad=comunidad, usuario=usuario)
    except:
        return []


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
        recibo_form = ReciboForm(request.POST)
        motivo_recibo_formset = MotivoReciboFormSet(request.POST)

        if gasto_form.is_valid() and recibo_form.is_valid() and motivo_recibo_formset.is_valid():
            # Guardar el gasto/incidencia
            gasto = gasto_form.save(commit=False)
            gasto.comunidad = comunidad
            gasto.save()

            # Guardar el recibo
            recibo = recibo_form.save(commit=False)
            recibo.comunidad = comunidad
            recibo.save()

            # Guardar los motivos del recibo
            for form in motivo_recibo_formset:
                motivo_recibo = form.save(commit=False)
                motivo_recibo.recibo = recibo
                motivo_recibo.save()

            return redirect('ruta_hacia_la_vista_donde_quieres_redirigir')
    else:
        gasto_form = GastoForm()
        recibo_form = ReciboForm()
        motivo_recibo_formset = MotivoReciboFormSet()

    return render(request, 'nombre_de_tu_template.html', {
        'gasto_form': gasto_form,
        'recibo_form': recibo_form,
        'motivo_recibo_formset': motivo_recibo_formset,
        'comunidad': comunidad,
    })





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


