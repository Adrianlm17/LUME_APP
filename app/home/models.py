from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    birthday = models.DateField(null=True, blank=True)
    fondo = models.CharField(max_length=20, default='clear')
    lang = models.CharField(max_length=10, default='es')
    user_rol = models.CharField(max_length=100, blank=True)
    IMG_profile = models.ImageField(default='anonimo.png')

    def __str__(self):
        return self.user.email



class Comunidad(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    portal = models.CharField(max_length=100)
    token = models.CharField(max_length=16, unique=True)
    IMG_profile = models.CharField(max_length=100, default='profiles/anonimo.png')
    dinero = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nombre



class Vivienda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    rol_comunidad = models.CharField(max_length=100, blank=True)
    piso = models.CharField(max_length=100)
    puerta = models.CharField(max_length=100)

    def __str__(self):
        return self.usuario.username


class Incidencia(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='incidencias/', null=True, blank=True)
    fecha_apertura = models.DateField(auto_now_add=True)
    prioridad = models.IntegerField(default=1)
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
    valoracion = models.IntegerField(null=True, blank=True)
    gasto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.titulo


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
    valoracion_media = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    IMG_profile = models.CharField(max_length=100, default='profiles/anonimo.png')

    def __str__(self):
        return self.nombre


class Trabajador(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username
    


class Evento(models.Model):
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField()

    def __str__(self):
        return self.titulo



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
    last_chat = models.CharField(max_length=100)
    read_by = models.ManyToManyField(User, related_name='read_chats', through='ChatReadBy')

    def __str__(self):
        return f"Chat {self.id} - From: {self.user.email} - To: {self.mensaje_user.email}"


class ChatReadBy(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
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



class Acta(models.Model):
    comunidad = models.ForeignKey('Comunidad', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.TextField()
    firmada = models.ForeignKey(User, on_delete=models.CASCADE)

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
    fecha_anuncio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    


# ------------------------------------------- GASTOS --------------------------------------------
class Recibo(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_tope = models.DateField()
    cantidad_total = models.DecimalField(max_digits=10, decimal_places=2)
    comunidad = models.ForeignKey('Comunidad', on_delete=models.CASCADE)

    def __str__(self):
        return f"Recibo: {self.titulo} - {self.fecha_tope}"
    
class Motivo(models.Model):
    TIPO_CHOICES = [
        ('luz', 'Luz'),
        ('agua', 'Agua'),
        ('gas', 'Gas'),
        ('piscina', 'Piscina'),
        ('jardineria', 'Jardinería'),
        ('personal_comunidad', 'Personal de comunidad'),
        ('limpieza', 'Limpieza'),
        ('extras', 'Extras'),
    ]

    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    recibo = models.ForeignKey(Recibo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo}: {self.cantidad}"

class Gasto(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    cantidad_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_tope = models.DateField()
    comunidad = models.ForeignKey('Comunidad', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

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

class UltimosMovimientos(models.Model):
    comunidad = models.ForeignKey('Comunidad', on_delete=models.CASCADE)

class ProximosPagos(models.Model):
    comunidad = models.ForeignKey('Comunidad', on_delete=models.CASCADE)

class PagosHechos(models.Model):
    comunidad = models.ForeignKey('Comunidad', on_delete=models.CASCADE)

class Historial(models.Model):
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    mes = models.CharField(max_length=100)



class SeguroComunidad(models.Model):
    comunidad = models.OneToOneField('Comunidad', on_delete=models.CASCADE)
    cubre = models.CharField(max_length=200)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateField(null=True)
    fecha_vencimiento = models.DateField()

    def __str__(self):
        estado = "Pagado" if self.pagado else "Pendiente"
        return f"Seguro de {self.comunidad.nombre} - Vencimiento: {self.fecha_vencimiento} ({estado})"