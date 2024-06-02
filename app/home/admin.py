from django.contrib import admin
from .models import UserProfile

# MODELs
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'IMG_profile')

admin.site.register(UserProfile, UserProfileAdmin)
