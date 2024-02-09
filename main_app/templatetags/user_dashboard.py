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


@register.filter
def calculate_average_rating(reviews):
    total_rating = sum([int(review.rating) for review in reviews])
    average_rating = total_rating / len(reviews) if reviews else 0
    return round(average_rating, 2)
