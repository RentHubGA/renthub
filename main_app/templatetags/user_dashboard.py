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

# @register.filter(name='reserve_status')
# def reserve_status(product, rented_product_ids, date_today):
#     for rented_id, rented_date_rent, rented_date_return in rented_product_ids:
#         if product.id == rented_id:
#             if date_today < rented_date_return and date_today < rented_date_rent:
#                 return 'Reserve'
#             elif date_today >= rented_date_return:
#                 return 'Available'
#             else:
#                 return 'Renting'

#     return 'Available'
