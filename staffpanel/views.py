from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from orders.models import Order
from inventory.models import FishItem
from users.models import CustomUser

@login_required
def staff_dashboard(request):
    # Staff can view recent orders and statistics
    orders = Order.objects.all().order_by('-date')[:20]
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    total_fish_items = FishItem.objects.count()
    low_stock_items = FishItem.objects.filter(stock__lt=10).count()
    
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_fish_items': total_fish_items,
        'low_stock_items': low_stock_items,
    }
    return render(request, 'staffpanel/dashboard.html', context)
