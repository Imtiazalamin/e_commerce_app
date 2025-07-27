from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from .views import profile_redirect

urlpatterns = [
   
    path('about/', views.about_view, name='about'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('account/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"),
    path('logout/', views.logout_view, name='logout_view'),
    path('accounts/profile/', profile_redirect, name='profile_redirect'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # Products
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_by_category'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('product/buy/<int:pk>/', views.buy_now, name='buy_now'),
    path('product/add/', views.add_product, name='add_product'),
    path('my-products/', views.my_products, name='my_products'),
    path('account/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', views.product_list, name='home'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
