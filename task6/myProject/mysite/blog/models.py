from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# 1. АБСТРАКТНАЯ МОДЕЛЬ

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        _('дата создания'),
        auto_now_add=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        _('дата обновления'),
        auto_now=True
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.__class__.__name__} #{self.id}"


# 2. МОДЕЛЬ КАТЕГОРИИ

class Category(TimeStampedModel):
    name = models.CharField(
        _('название'),
        max_length=100,
        unique=True
    )
    description = models.TextField(
        _('описание'),
        blank=True
    )
    is_active = models.BooleanField(
        _('активна'),
        default=True
    )

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('категории')
        ordering = ['name']

    def __str__(self):
        return self.name


# 3. МОДЕЛЬ ТОВАРА

class Product(TimeStampedModel):
    name = models.CharField(
        _('название'),
        max_length=200
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('категория')
    )
    price = models.DecimalField(
        _('цена'),
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField(
        _('описание'),
        blank=True
    )
    quantity = models.PositiveIntegerField(
        _('количество'),
        default=0
    )
    is_available = models.BooleanField(
        _('в наличии'),
        default=True
    )

    class Meta:
        verbose_name = _('товар')
        verbose_name_plural = _('товары')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"


# 4. МОДЕЛЬ ОТЗЫВА

class Review(TimeStampedModel):
    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('товар')
    )
    author_name = models.CharField(
        _('имя автора'),
        max_length=100
    )
    email = models.EmailField(
        _('email'),
        blank=True
    )
    rating = models.PositiveIntegerField(
        _('рейтинг'),
        choices=RATING_CHOICES,
        default=5
    )
    comment = models.TextField(
        _('комментарий')
    )
    is_published = models.BooleanField(
        _('опубликован'),
        default=True
    )

    class Meta:
        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв от {self.author_name} на {self.product.name}"