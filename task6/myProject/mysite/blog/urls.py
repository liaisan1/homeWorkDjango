from django.urls import path
from . import views

urlpatterns = [
    # Главная
    path('', views.home, name='home'),

    # Списки
    path('categories/', views.category_list, name='category_list'),
    path('products/', views.product_list, name='product_list'),
    path('reviews/', views.review_list, name='review_list'),

    # Добавление через Faker
    path('categories/add/', views.add_random_category, name='add_random_category'),
    path('products/add/', views.add_random_product, name='add_random_product'),
    path('reviews/add/', views.add_random_review, name='add_random_review'),

    # Удаление
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),

    # Детальные страницы
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('reviews/<int:review_id>/', views.review_detail, name='review_detail'),
]