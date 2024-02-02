from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Product, Image, Review, Renting, CustomUser

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Review)
admin.site.register(Renting)
admin.site.register(CustomUser, UserAdmin)

# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'user')  # Make sure 'user' is the correct attribute name

# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(UserAdmin)