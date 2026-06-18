from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from orders.models import Order

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalog:product_list')
    else:
        form = RegisterForm()
    return render(
        request,
        'users/register.html',
        {'form': form}
    )
@login_required
def profile_view(request):
    orders = Order.objects.filter(
        user = request.user
    ).order_by('created_at')
    return render(
        request, 'users/profile.html',
        {'orders': orders}
    )