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

# fieldsets = (
#     (None, {'fields': ('username', 'email', 'password')}),
#     ('Personal Info', {'fields': ('first_name', 'last_name', 'avatar', 'address', 'town', 'county', 'post_code', 'country')}),
#     ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#     ('Important dates', {'fields': ('last_login', 'date_joined')}),
# )
# add_fieldsets = (
#     (None, {
#         'classes': ('wide',),
#         'fields': ('username', 'email', 'password1', 'password2'),
#     }),
# )

# admin.site.register(CustomUser, CustomUserAdmin)