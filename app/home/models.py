from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    birthday = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    floor = models.CharField(max_length=100, blank=True)
    door = models.CharField(max_length=100, blank=True)
    img_profile = models.ImageField(upload_to='profiles/', blank=True)
    lang = models.CharField(max_length=10, default='es')
    user_rol = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username