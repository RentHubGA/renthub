from django.urls import path
from . import views
from .views import get_unavailable_dates


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<int:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('products/<int:pk>/rent_product/', views.rent_product, name='rent_product'),
    path('products/create/', views.ProductCreate.as_view(), name='product_create'),
    path('products/<int:pk>/update', views.ProductUpdate.as_view(), name='product_update'),
    path('products/<int:pk>/delete', views.ProductDelete.as_view(), name='product_delete'),
    path('products/<int:pk>/review', views.ReviewCreate.as_view(), name='review_create'),
    # path('products/<int:pk>/add_image', views.add_image, name='add_image'),
    path('get_unavailable_dates/<int:product_id>/', get_unavailable_dates, name='get_unavailable_dates'),
    ## accounts Root
    path('accounts/profile/<str:username>/detail', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('accounts/profile/<str:username>/', views.Profile.as_view(), name='profile' ),
    path('accounts/profile/<str:username>/dashboard/', views.ProfileDashboard.as_view(), name='profile_dashboard'),
    path('accounts/profile/<str:username>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('accounts/register/', views.register, name='register'),
]