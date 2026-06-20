from django.contrib import admin
from django.urls import path
from sellerapp import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('add_product/',views.add_product,name="add_product"),
    path('view-products/', views.view_products, name='view_products'),
    path('product_details/<int:pid>/', views.product_details, name="product_details"),
    path('edit_product/<int:pid>/', views.edit_product, name="edit_product"),
    path('delete_product/<int:pid>/', views.delete_product, name="delete_product"),
    path('add_category/', views.add_category, name='add_category'),
    path('view_categories/', views.view_categories, name='view_categories'),
    path('edit_profile/', views.edit_profile, name='edit_profile'), 
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('edit_category/<int:cid>/', views.edit_category, name="edit_category"),
    path('delete_category/<int:cid>/', views.delete_category, name="delete_category"),
    path('userpanel/', views.userpanel, name='userpanel'),
    path('index/', views.index, name='index'),
    path('updated/<int:pid>', views.updated, name='updated'),
    path('categories_product', views.categories_product, name='categories_product'),
    path('cart', views.cart, name='cart'),
    path('add-to-cart<int:pk>', views.add_to_cart, name='add-to-cart'),
    path('checkout', views.checkout, name='checkout'),
]
