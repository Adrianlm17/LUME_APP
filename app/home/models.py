from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    birthday = models.DateField(null=True, blank=True)
    fondo = models.CharField(max_length=20, default='clear')
    lang = models.CharField(max_length=10, default='es')
    user_rol = models.CharField(max_length=100, blank=True)
    IMG_profile = models.ImageField(upload_to='profiles', default='profiles/anonimo.png')

    def __str__(self):
        return self.user.username


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
    piso = models.CharField(max_length=100)
    puerta = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.comunidad.nombre}, {self.piso} {self.puerta}"


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
        return f"{self.usuario.username} - {self.empresa.nombre}"


class Gasto(models.Model):
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Gasto en {self.comunidad.nombre}: ${self.monto} - {self.fecha}"


class Transaccion(models.Model):
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Transaccion en {self.comunidad.nombre}: ${self.monto} - {self.fecha}"


class Evento(models.Model):
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField()

    def __str__(self):
        return self.titulo
