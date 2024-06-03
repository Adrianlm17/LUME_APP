from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from taggit.managers import TaggableManager





class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(null=True, max_length=20, blank=True)
    birthday = models.DateField(null=True, blank=True)
    fondo = models.CharField(max_length=20, default='clear')
    lang = models.CharField(max_length=10, default='es')
    user_rol = models.CharField(max_length=100, blank=True)
    IMG_profile = models.ImageField(upload_to='perfiles/', default='perfiles/anonimo.png')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.email




class Comunidad(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    dirrecion = models.CharField(max_length=100)
    portal = models.CharField(max_length=100)
    token = models.CharField(max_length=16, unique=True)
    IMG_profile = models.ImageField(upload_to='perfiles/', default='perfiles/anonimo.png')
    dinero = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    metodo_pago = models.CharField(max_length=50, choices=[('igual', 'Pagar por igual'), ('coeficientes', 'Pagar por coeficientes')], default='igual')
    numero_cuenta = models.CharField(max_length=20, unique=True, null=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nombre




class Vivienda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    ROL_COMUNIDAD = [
        ('community_president', 'Community President'),
        ('community_vicepresident', 'Community Vice President'),
        ('community_user', 'Community User'),
    ]
    rol_comunidad = models.CharField(max_length=100, choices=ROL_COMUNIDAD, default='community_user')
    piso = models.CharField(max_length=100)
    puerta = models.CharField(max_length=100)
    porcentaje_pago = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.usuario.username



class Incidencia(models.Model):
    numero = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='incidencias/', null=True, blank=True)
    fecha_apertura = models.DateField(auto_now_add=True)
    fecha_cierre = models.DateField(null=True, blank=True)
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='baja')
    ESTADO_CHOICES = [
        ('Pendiente de aceptar', 'Pendiente de aceptar'),
        ('Denegada', 'Denegada'),
        ('Aceptada', 'Aceptada'),
        ('Asignada', 'Asignada'),
        ('Cancelada', 'Cancelada'),
        ('Trabajando', 'Trabajando'),
        ('Terminada', 'Terminada'),
        ('Finalizada', 'Finalizada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente de aceptar')
    empresa = models.ForeignKey('Empresa', on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, null=True)
    valoracion = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)], default=3)
    gasto = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.00)

    def __str__(self):
        return f"#{self.numero} - {self.titulo}"

    def save(self, *args, **kwargs):
        if self.estado == 'Finalizada' and not self.fecha_cierre:
            self.fecha_cierre = timezone.now().date()
        super().save(*args, **kwargs)


class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=254)
    pais = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    token = models.CharField(max_length=16, unique=True)
    valoracion_media = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(10)])
    IMG_profile = models.ImageField(upload_to='perfiles/', default='perfiles/anonimo.png')
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.nombre
    

class Trabajador(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username
    

class Evento(models.Model):
    PUBLIC = 'publico'
    PRIVATE = 'privado'
    VISIBILITY_CHOICES = [
        (PUBLIC, 'Publico'),
        (PRIVATE, 'Privado'),
    ]

    title = models.CharField(max_length=255)
    descripcion = models.TextField()
    date = models.DateField(blank=True)
    max_attendees = models.PositiveIntegerField(null=True)
    current_attendees = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='eventos/', blank=True, null=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default=PUBLIC)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title



class Asistencias(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('evento', 'usuario')



class Nota(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo



class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    mensaje_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensaje_user')
    titulo = models.CharField(max_length=100)
    IMG_profile = models.ImageField(upload_to='chat/', default='chat/anonimo.png')
    last_chat = models.CharField(max_length=100)
    read_by = models.ManyToManyField(User, related_name='read_chats', through='ChatReadBy')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Chat {self.id} - From: {self.user.email} - To: {self.mensaje_user.email}"



class GroupChat(models.Model):
    title = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='group_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    last_chat = models.CharField(max_length=100, null=True)
    IMG_profile = models.ImageField(upload_to='chat/', default='chat/anonimo.png')
    read_by = models.ManyToManyField(User, related_name='read_groups', through='GroupReadBy')

    def __str__(self):
        return self.title



class Message(models.Model):
    group_chat = models.ForeignKey(GroupChat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.user.username}'



class ChatReadBy(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = (('chat', 'user'),)

    def __str__(self):
        status = "Read" if self.is_read else "Unread"
        return f"Chat {self.chat.id} read by {self.user.email}: {status}"



class GroupReadBy(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = (('chat', 'user'),)

    def __str__(self):
        status = "Read" if self.is_read else "Unread"
        return f"Chat {self.chat.id} read by {self.user.email}: {status}"



class ExtendsChat(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()
    user_send = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Extendido Chat {self.chat.id} - {self.text[:20]}"
    


class ExtendsGroupChat(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    text = models.TextField()
    user_send = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Extendido Chat {self.chat.id} - {self.text[:20]}"


class Acta(models.Model):
    comunidad = models.ForeignKey('Comunidad', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.TextField()
    firmada = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='actas/', null=True, blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.comunidad}"
    


class Calendario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, null=True)
    fecha = models.DateField()
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True)
    evento = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.titulo



class Anuncio(models.Model):
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_anuncio = models.DateField(blank=True)

    def __str__(self):
        return self.titulo
    


class CalendarioLimpieza(models.Model):
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True)
    zona = models.CharField(max_length=200)
    fecha = models.DateField()
    usuarios_asignados = models.ManyToManyField(User, related_name='tareas_limpieza')

    def __str__(self):
        return f"{self.titulo} - {self.comunidad.nombre}"
    


# ------------------------------------------- GASTOS --------------------------------------------
class Recibo(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    fecha_tope = models.DateField(null=True)
    cantidad_total = models.DecimalField(max_digits=10, decimal_places=2)
    comunidad = models.ForeignKey('Comunidad', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='recibos/', null=True, blank=True)

    def __str__(self):
        return f"Recibo: {self.titulo} - {self.fecha_tope}"
    


class Motivo(models.Model):
    TIPO_CHOICES = [
        ('luz', 'Luz'),
        ('agua', 'Agua'),
        ('gas', 'Gas'),
        ('piscina', 'Piscina'),
        ('jardineria', 'Jardinería'),
        ('personal', 'Personal de comunidad'),
        ('limpieza', 'Limpieza'),
        ('seguro', 'Seguro Comunidad'),
        ('fondos', 'Fondos para la Comunidad'),
        ('extras', 'Extras'),
    ]

    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    recibo = models.ForeignKey(Recibo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo}: {self.cantidad}"



class Gasto(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    cantidad_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_tope = models.DateField(null=True)
    fecha = models.DateField()
    comunidad = models.ForeignKey('Comunidad', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    archivo = models.FileField(upload_to='gastos/', null=True, blank=True)
    ESTADO_CHOICES = [
        ('pagado', 'Pagado'),
        ('pendiente', 'Pendiente')
    ]
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="pendiente")

    def __str__(self):
        return f"Gasto: {self.titulo} - {self.fecha_tope}"



class MotivoRecibo(models.Model):
    recibo = models.ForeignKey(Recibo, on_delete=models.CASCADE, related_name='motivos')
    tipo = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tipo}: {self.cantidad}"



class Transaccion(models.Model):
    comunidad = models.ForeignKey('Comunidad', on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.CharField(max_length=100, null=True)



class PagosUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comunidad = models.ForeignKey('Comunidad', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_pagada = models.DecimalField(max_digits=10, null=True, decimal_places=2)
    ESTADO_CHOICES = [
        ('pagado', 'Pagado'),
        ('pendiente', 'Pendiente')
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    archivo = models.FileField(upload_to='pagos/', null=True, blank=True)

    def __str__(self):
        return f"Pago: {self.cantidad} - {self.fecha}"



class SeguroComunidad(models.Model):
    empresa = models.CharField(max_length=200, null=True)
    comunidad = models.OneToOneField('Comunidad', on_delete=models.CASCADE)
    cubre = models.TextField()
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateField()
    fecha_vencimiento = models.DateField()

    def __str__(self):
        estado = "Pagado" if self.pagado else "Pendiente"
        return f"Seguro de {self.comunidad.nombre} - Vencimiento: {self.fecha_vencimiento} ({estado})"



class Notificacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=255)
    url = models.URLField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
