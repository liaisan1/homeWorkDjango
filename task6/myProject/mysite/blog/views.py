from django.shortcuts import render, get_object_or_404, redirect
from faker import Faker
from .models import Category, Product, Review

fake = Faker('ru_RU')

# ГЛАВНАЯ
def home(request):
    return render(request, 'blog/home.html', {
        'categories_count': Category.objects.count(),
        'products_count': Product.objects.count(),
        'reviews_count': Review.objects.count(),
    })

# СПИСКИ
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'blog/product_list.html', {'products': products})

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'blog/review_list.html', {'reviews': reviews})

#  ДОБАВЛЕНИЕ
def add_random_category(request):
    category = Category.objects.create(
        name=fake.word().capitalize(),
        description=fake.text(max_nb_chars=100),
        is_active=True
    )
    return redirect('category_list')

def add_random_product(request):
    categories = Category.objects.all()
    if categories.exists():
        category = fake.random_element(categories)
        product = Product.objects.create(
            name=fake.catch_phrase(),
            category=category,
            price=round(fake.random.uniform(100, 5000), 2),
            description=fake.text(max_nb_chars=200),
            quantity=fake.random_int(min=1, max=50),
            is_available=True
        )
        return redirect('product_list')
    return redirect('category_list')

def add_random_review(request):
    products = Product.objects.all()
    if products.exists():
        product = fake.random_element(products)
        review = Review.objects.create(
            product=product,
            author_name=fake.name(),
            email=fake.email(),
            rating=fake.random_int(min=1, max=5),
            comment=fake.text(max_nb_chars=150),
            is_published=True
        )
        return redirect('review_list')
    return redirect('product_list')

#УДАЛЕНИЕ
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_list')

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect('review_list')

# ДЕТАЛЬНЫЕ СТРАНИЦЫ
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'blog/category_detail.html', {'category': category})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'blog/product_detail.html', {'product': product})

def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    return render(request, 'blog/review_detail.html', {'review': review})