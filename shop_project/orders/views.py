from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            send_order_receipt(order)
            cart.clear()
            return render(request, 'orders/order_created.html', {
                'order': order
            })
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'form': form
    })

def send_order_receipt(order):
    subject = f'Your receipt for order #{order.id}'
    message = f'Order #{order.id}\n\n'
    message += f'Name: {order.full_name}\n'
    message += f'Address: {order.address}\n\n'
    message += 'Items:\n'

    for item in order.items.all():
        message += f'- {item.product.name} * {item.quantity} = {item.get_cost()}\n'
    message += f'\nTotal: {order.get_total_price()}'
    send_mail(
        subject,
        message,
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@example.com'),
        [order.email],
        fail_silently=False
    )

# Create your views here.
