import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from blog.models import Post

print("=" * 50)
print("СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ")
print("=" * 50)

Post.objects.all().delete()
print("Удалены старые посты")

posts = [
    ("Первый пост", "Привет! Это мой первый пост в блоге."),
    ("Второй пост", "Продолжаем изучать веб-разработку."),
    ("Третий пост", "Django делает разработку веб-приложений простой."),
]

for title, content in posts:
    Post.objects.create(
        title=title,
        content=content,
        is_published=True
    )
    print(f"Создан: {title}")

print("=" * 50)
print(f"Всего постов: {Post.objects.count()}")
print("=" * 50)