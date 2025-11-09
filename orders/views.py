from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, Order
from inventory.models import FishItem


@login_required
def view_cart(request):
    items = Cart.objects.filter(user=request.user)
    # Calculate subtotals for each item
    cart_data = []
    total = 0
    for item in items:
        subtotal = item.fish_item.price_per_kg * item.quantity
        total += subtotal
        cart_data.append({
            'item': item,
            'subtotal': subtotal
        })
    return render(request, 'orders/cart.html', {'cart_data': cart_data, 'total': total})


@login_required
def add_to_cart(request, fish_id):
    fish = get_object_or_404(FishItem, id=fish_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        messages.error(request, 'Quantity must be greater than 0')
        return redirect('inventory_list')
    
    if quantity > fish.stock:
        messages.error(request, f'Only {fish.stock} kg available in stock')
        return redirect('inventory_list')
    
    # Get or create cart item
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        fish_item=fish,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Update quantity if item already in cart
        cart_item.quantity += quantity
        if cart_item.quantity > fish.stock:
            cart_item.quantity = fish.stock
            messages.warning(request, f'Updated quantity to available stock: {fish.stock} kg')
        cart_item.save()
        messages.success(request, f'Updated cart: {fish.name}')
    else:
        messages.success(request, f'Added {fish.name} to cart')
    
    return redirect('view_cart')


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    fish_name = cart_item.fish_item.name
    cart_item.delete()
    messages.success(request, f'Removed {fish_name} from cart')
    return redirect('view_cart')


@login_required
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, 'Item removed from cart')
    elif quantity > cart_item.fish_item.stock:
        messages.error(request, f'Only {cart_item.fish_item.stock} kg available')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated')
    
    return redirect('view_cart')


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('view_cart')
    
    # Calculate total
    total = sum([item.fish_item.price_per_kg * item.quantity for item in cart_items])
    
    # Check stock availability
    for item in cart_items:
        if item.quantity > item.fish_item.stock:
            messages.error(request, f'Insufficient stock for {item.fish_item.name}. Only {item.fish_item.stock} kg available')
            return redirect('view_cart')
    
    # Create order
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        status='Pending'
    )
    
    # Create order items and update stock
    from orders.models import OrderItem
    for item in cart_items:
        fish = item.fish_item
        # Create order item before updating stock
        OrderItem.objects.create(
            order=order,
            fish_item=fish,
            quantity=item.quantity,
            price=fish.price_per_kg
        )
        # Update stock
        fish.stock -= item.quantity
        fish.save()
        # Remove from cart
        item.delete()
    
    messages.success(request, f'Order placed successfully! Order #{order.id}')
    return redirect('order_success', order_id=order.id)


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
