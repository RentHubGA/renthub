from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.


# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'user')  # Make sure 'user' is the correct attribute name

# admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomUser, UserAdmin)
# admin.site.register(UserAdmin)