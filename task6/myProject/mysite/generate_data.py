import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from blog.models import Category, Product, Review


def create_test_data():
    print("Создание тестовых данных...")

    # 1. Создаем категории
    categories_data = [
        ("Электроника", "Техника и гаджеты"),
        ("Одежда", "Модная одежда и аксессуары"),
        ("Книги", "Литература разных жанров"),
        ("Продукты", "Пищевые продукты"),
        ("Спорт", "Спортивные товары"),
    ]

    categories = []
    for name, desc in categories_data:
        category = Category.objects.create(
            name=name,
            description=desc,
            is_active=True
        )
        categories.append(category)
        print(f"✓ Создана категория: {name}")

    # 2. Создаем товары
    products_data = [
        ("Смартфон", 29999.99, 50, categories[0]),
        ("Ноутбук", 69999.99, 20, categories[0]),
        ("Футболка", 1499.99, 100, categories[1]),
        ("Джинсы", 3999.99, 60, categories[1]),
        ("Роман", 599.99, 200, categories[2]),
        ("Учебник", 1299.99, 150, categories[2]),
        ("Молоко", 89.99, 300, categories[3]),
        ("Хлеб", 49.99, 500, categories[3]),
        ("Мяч", 1999.99, 80, categories[4]),
        ("Гантели", 2999.99, 40, categories[4]),
    ]

    products = []
    for name, price, quantity, category in products_data:
        product = Product.objects.create(
            name=name,
            category=category,
            price=price,
            description=f"Описание товара {name}",
            quantity=quantity,
            is_available=True
        )
        products.append(product)
        print(f"✓ Создан товар: {name} - {price} руб.")

    # 3. Создаем отзывы
    reviews_data = [
        ("Анна", 5, "Отличный товар!"),
        ("Иван", 4, "Хорошо, но есть недостатки"),
        ("Мария", 5, "Очень доволен покупкой"),
        ("Алексей", 3, "Нормально, но ожидал большего"),
        ("Ольга", 5, "Супер! Рекомендую всем"),
    ]

    for author, rating, comment in reviews_data:
        product = random.choice(products)
        Review.objects.create(
            product=product,
            author_name=author,
            email=f"{author.lower()}@example.com",
            rating=rating,
            comment=comment,
            is_published=True
        )
        print(f"Создан отзыв от {author} на {product.name}")

    print("\n" + "=" * 50)
    print("Данные созданы успешно!")
    print(f"   Категорий: {Category.objects.count()}")
    print(f"   Товаров: {Product.objects.count()}")
    print(f"   Отзывов: {Review.objects.count()}")
    print("=" * 50)


if __name__ == '__main__':
    create_test_data()