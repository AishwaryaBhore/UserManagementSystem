from django.contrib import admin
from .models import CustomUser
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone_number',)


admin.site.register(CustomUser, UserAdmin)
