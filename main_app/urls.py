from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<int:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('products/create/', views.ProductCreate.as_view(), name='product_create'),
    path('reviewform/', views.reviewform, name='reviewform'),
    path('products/<int:pk>/add_image', views.add_image, name='add_image'),
    ## accounts Root
    path('accounts/profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('accounts/profile/<int:pk>/update', views.ProfileUpdate.as_view(), name='profile_update'),
    path('accounts/register/', views.register, name='register'),
]