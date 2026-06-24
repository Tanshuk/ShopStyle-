"""Product views."""
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def product_list_view(request):
    """Display all products with filtering."""
    products = Product.objects.all()
    
    # Filter by gender
    gender = request.GET.get('gender')
    if gender:
        products = products.filter(gender=gender)
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        products = products.filter(category__slug=category)
    
    # Filter by sale
    if request.GET.get('sale') == 'true':
        products = products.filter(is_on_sale=True)
    
    # Search
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    context = {
        'products': products,
        'title': 'Products',
        'total_products': products.count(),
    }
    return render(request, 'products/product_list.html', context)

def product_detail_view(request, slug):
    """Display a single product."""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
        'title': product.name,
    }
    return render(request, 'products/product_detail.html', context)

def product_search_view(request):
    """Search products."""
    query = request.GET.get('q', '')
    products = Product.objects.none()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    context = {
        'products': products,
        'query': query,
        'title': f'Search Results for "{query}"',
    }
    return render(request, 'products/search_results.html', context)

def categories_view(request):
    """Display all categories."""
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'title': 'All Categories',
    }
    return render(request, 'products/categories.html', context)