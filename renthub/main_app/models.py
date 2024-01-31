from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import AbstractUser

# Create your models here...



RATINGS = (
    ('5', 'Execellent'),
    ('4', 'Very good'),
    ('3', 'Ok'),
    ('2', 'Bad'),
    ('1', 'Very bad'),
)


# User Model
class User(AbstractUser):
    name = models.CharField(max_length=50)
    avatar = models.URLField(max_length=200)
    address = models.CharField(
        verbose_name='Address',max_length=150, null=True, blank=False
        )
    town = models.CharField(
        verbose_name='Town/City',max_length=150, null=True, blank=False
        )
    county = models.CharField(
        verbose_name='County',max_length=150, null=True, blank=False
        )
    post_code = models.CharField(
        verbose_name='Post Code',max_length=150, null=True, blank=False
        )
    country = models.CharField(
        verbose_name='Country',max_length=150, null=True, blank=False
        )
    #
    # location = models.PointField(null=True, blank=True)
    #

    def __str__(self):
        return self.user

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_id': self.id})


# Product Model
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    price = models.PositiveIntegerField()
    available = models.BooleanField()
    # many to many Category
    category = models.ManyToManyField(Category)
    # one to many User
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.product_name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'product_id': self.id})
    
    # get average rating to show on product
    def get_average(self):
        reviews_num = self.review_set.count()
        pass

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
        max_length=20,
        choices=RATINGS,
        default=RATINGS[0][0]
    )
    # one to many Product
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    # one to many User
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user} review: {self.product} {self.rating}'
    
    class Meta:
        ordering = ['-date']


# Renting Model
class Renting(models.Model):
    date_rent = models.DateField('Renting Date')
    date_return = models.DateField('Return Date')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # one to many Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # one to many User
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return  f'{self.user.name} {self.product} ({self.date_rent}) - ({self.date_return}), Total Price: {self.total_price}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'renting_id': self.id})
    
    class Meta:
        ordering = ['-date_rent']
