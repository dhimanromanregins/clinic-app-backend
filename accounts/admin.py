from django.contrib import admin
from .models import CustomUser, Profile, Banner
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Banner)
