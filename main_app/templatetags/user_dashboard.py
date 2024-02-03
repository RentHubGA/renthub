from django import template
from ..models import Product, Renting
from datetime import date
from django.contrib import messages
register=template.Library()

@register.simple_tag
def user_products(user):
    products = Product.objects.filter(user=user)
    return products

@register.simple_tag
def user_rent(user):
    return user.renting_set.all()
