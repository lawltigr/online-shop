from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request,  category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    q = request.GET.get('q')
    if q:
        products = products.filter(name__icontains=q)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=min_price)
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass
    in_stock = request.GET.get('in_stock')
    if in_stock == '1':
        products = products.filter(stock__gt=0)
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'catalog/product_detail.html', {'product': product})

# Create your views here.
