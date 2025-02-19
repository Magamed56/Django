from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'categories': categories, 'products': products})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'store/product_list.html', {'categories': categories, 'products': products, 'selected_category': category})
