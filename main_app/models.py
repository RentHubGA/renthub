from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
# Create your models here...
# User = get_user_model()


RATINGS = (
    ('5', 'Execellent'),
    ('4', 'Very good'),
    ('3', 'Ok'),
    ('2', 'Bad'),
    ('1', 'Very bad'),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        # Create normal user Email Require
        if not email:
            raise ValueError('The Email field must be set')
        # else:
        email = self.normalize_email(email)

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user
    
        # Create superuser user, password, email
    def create_superuser(self, email, username, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)
    

# User Model
class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    avatar = models.URLField(max_length=200)
    address = models.CharField(
        verbose_name='Address',max_length=150, null=True, blank=True
        )
    town = models.CharField(
        verbose_name='Town/City',max_length=150, null=True, blank=True
        )
    county = models.CharField(
        verbose_name='County',max_length=150, null=True, blank=True
        )
    post_code = models.CharField(
        verbose_name='Post Code',max_length=150, null=True, blank=True
        )
    country = models.CharField(
        verbose_name='Country',max_length=150, null=True, blank=True
        )
    # >>>>> add user fixing admin user error <<<<<
    user = models.CharField(max_length=255, null=False)
    #
    # location = models.PointField(null=True, blank=True)
    #
    objects = CustomUserManager()

    def __str__(self):
        return self.username

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
    # many to many Category
    category = models.ManyToManyField(Category)
    # one to many User
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return  f'{self.user.name} {self.product} ({self.date_rent}) - ({self.date_return}), Total Price: {self.total_price}'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'renting_id': self.id})
    
    class Meta:
        ordering = ['-date_rent']
