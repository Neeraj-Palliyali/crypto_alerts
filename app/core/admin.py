from django.contrib import admin
from .models import UserAlert
# Register your models here.
class UserAlertAdmin(admin.ModelAdmin):
    model = UserAlert
    list_display = ( 'user', 'limit')

admin.site.register(UserAlert, UserAlertAdmin)