from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from orders.models import Order, OrderItem
from catalog.models import Product

@staff_member_required
def dashboard_view(request):
    total_orders = Order.objects.count()
    total_revenue = (
        OrderItem.objects.aggregate(
            revenue=Sum('price')
        )['revenue'] or 0
    )
    total_users = User.objects.count()
    total_products = Product.objects.count()
    top_products = (
        OrderItem.objects
        .values('product__name')
        .annotate(total_sold=Count('id'))
        .order_by('-total_sold')[:5]
    )
    orders_by_day=(
        Order.objects
        .extra({'day': "date(created_at)"})
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )
    labels = [item['day'].strftime('%Y-%m-%d') for item in orders_by_day]
    data = [item['count'] for item in orders_by_day]
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_products': total_products,
        'top_products': top_products,
        'labels': labels,
        'data': data,
    }
    return render(request, 'dashboard/dashboard.html', context)