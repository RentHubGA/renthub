from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.gis.db.models import PointField


# Create your models here.



RATINGS = (
    ('5'),
    ('4'),
    ('3'),
    ('2'),
    ('1'),
    ('0'),
)

# User Model
class User(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    # not sure about location
    location = models.PointField(geography=True, spatial_index=True)


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_id': self.id})


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    price = models.PositiveIntegerField()
    available = models.BooleanField()
    # many to many Category
    category = models.ManyToManyField(Category)
    # one to many User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'product_id': self.id})


# Image Model
class Image(models.Model):
    url = models.URLField(max_length=200)
    # one to many Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for product_id: {self.product_id} @{self.url}"


# Review Model
class Review(models.Model):
    date = models.DateField('Review Date')
    description = models.TextField(max_length=255)
    rating = models.CharField(
        max_length=1,
        choice=RATINGS,
        required=True
    )
    # one to many Product
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    # one to many User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} review: {self.product} {self.rating}'
    
    class Meta:
        ordering = ['-date']


# Renting Model
class Renting(models.Model):
    date_rent = models.DateField('Renting Date')
    date_return = models.DateField('Return Date')
    total_price = models.PositiveBigIntegerField()
    # one to many Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # one to many User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return  f'{self.user} {self.product} ({self.date_rent}) - ({self.date_return}), Total Price: {self.total_price}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'renting_id': self.id})
    
    class Meta:
        ordering = ['-date']