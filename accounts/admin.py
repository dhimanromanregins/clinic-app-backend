from django.contrib import admin
from .models import CustomUser, Profile, Banner,Notifications
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Banner)
admin.site.register(Notifications)
