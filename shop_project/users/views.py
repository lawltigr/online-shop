from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from orders.models import Order
from django.contrib import messages
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Wishlist, Product

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
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance = profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    orders = Order.objects.filter(
        user = request.user
    ).order_by('created_at')
    return render(
        request, 'users/profile.html',
        {'orders': orders, 'user_form': user_form, 'profile_form': profile_form}
    )

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'users/wishlist.html', {
        'wishlist_items': wishlist_items
    })

@login_required
def wishlist_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    return redirect('users:wishlist')

@login_required
def wishlist_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(
        user=request.user,
        product=product
    ).delete()
    return redirect('users:wishlist')