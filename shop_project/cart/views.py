from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Product
from .cart import Cart

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart':cart})

def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action')
    if action == 'increase':
        cart.add(product=product, quantity=1)
    elif action == 'decrease':
        current_qty = cart.cart.get(str(product.id), {}).get('quantity', 1)
        if current_qty > 1:
            cart.add(product=product, quantity=1, update_quantity=False)
            cart.cart[str(product.id)]['quantity']-=2
        else:
            cart.remove(product)
    return redirect('cart:cart_detail')