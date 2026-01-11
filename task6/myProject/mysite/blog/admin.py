from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Review


# 1. КАТЕГОРИИ

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'products_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')

    def products_count(self, obj):
        return obj.products.count()

    products_count.short_description = 'Количество товаров'


# 2. ТОВАРЫ

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity',
                    'is_available', 'created_at')
    list_filter = ('is_available', 'category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'quantity', 'is_available')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'description')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'quantity', 'is_available')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# 3. ОТЗЫВЫ


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'product', 'rating_stars',
                    'is_published', 'created_at')
    list_filter = ('is_published', 'rating', 'created_at')
    search_fields = ('author_name', 'comment', 'product__name')
    list_editable = ('is_published',)
    readonly_fields = ('created_at', 'updated_at')

    def rating_stars(self, obj):
        stars = '★' * obj.rating
        return format_html('<span style="color: gold; font-size: 16px;">{}</span>', stars)

    rating_stars.short_description = 'Рейтинг'