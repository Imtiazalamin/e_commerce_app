from django.urls import path
from . import views

app_name = 'ecommerceapp'  # namespace যোগ করা ভালো প্র্যাকটিস

urlpatterns = [
    # পাবলিক ভিউস
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('about/', views.about, name='about'),
    path('search/', views.product_search, name='product_search'),
    
    # অথেনটিকেশন রিলেটেড
    path('seller/register/', views.seller_register, name='seller_register'),
    
    # লগিন রিকোয়ারড ভিউস (সেলার ভিউস)
    path('product/add/', views.add_product, name='add_product'),
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),  # id থেকে pk তে পরিবর্তন
    path('product/delete/<int:pk>/', views.deleteproduct, name='deleteproduct'),  # id থেকে pk তে পরিবর্তন
    path('seller/products/', views.seller_products, name='seller_products'),
    
    # ইউজার একশনস
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.cart, name='cart'),
]