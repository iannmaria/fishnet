from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import CustomUser
from fishermen.models import FishermanProfile, Complaint
from inventory.models import FishItem
from orders.models import Order
from django.db.models import Sum, Count

# Only admin access
def admin_required(user):
    return user.is_superuser

@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    # Count customers (users who are not superuser, not staff, and role is customer)
    customer_count = CustomUser.objects.filter(
        is_superuser=False, 
        is_staff=False,
        role='customer'
    ).count()
    
    context = {
        "fishermen_count": FishermanProfile.objects.count(),
        "user_count": customer_count,
        "staff_count": CustomUser.objects.filter(is_staff=True, is_superuser=False).count(),
        "fish_count": FishItem.objects.count(),
        "order_count": Order.objects.count(),
    }
    return render(request, "adminpanel/dashboard.html", context)


# ---- Fisherman Management ----
@login_required
@user_passes_test(admin_required)
def view_fishermen(request):
    fishermen = FishermanProfile.objects.all().order_by('-registration_date')
    return render(request, "adminpanel/fisherman_list.html", {"fishermen": fishermen})


@login_required
@user_passes_test(admin_required)
def view_fisherman_detail(request, fisherman_id):
    fisherman = get_object_or_404(FishermanProfile, id=fisherman_id)
    return render(request, "adminpanel/fisherman_detail.html", {"fisherman": fisherman})


@login_required
@user_passes_test(admin_required)
def approve_fisherman(request, fisherman_id):
    fisherman = get_object_or_404(FishermanProfile, id=fisherman_id)
    fisherman.status = "Approved"
    fisherman.save()
    return redirect("view_fishermen")


@login_required
@user_passes_test(admin_required)
def remove_fisherman(request, fisherman_id):
    fisherman = get_object_or_404(FishermanProfile, id=fisherman_id)
    fisherman.delete()
    return redirect("view_fishermen")


# ---- User Management ----
@login_required
@user_passes_test(admin_required)
def view_users(request):
    users = CustomUser.objects.filter(is_superuser=False, is_staff=False, role='customer')
    return render(request, "adminpanel/user_list.html", {"users": users})


@login_required
@user_passes_test(admin_required)
def remove_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect("view_users")


# ---- Staff Management ----
@login_required
@user_passes_test(admin_required)
def view_staff(request):
    staff = CustomUser.objects.filter(is_staff=True, is_superuser=False)
    return render(request, "adminpanel/staff_list.html", {"staff": staff})


@login_required
@user_passes_test(admin_required)
def assign_region_to_staff(request, staff_id):
    staff = get_object_or_404(CustomUser, id=staff_id)
    staff.region = "Kochi Port"  # Example function
    staff.save()
    return redirect("view_staff")



# ---- Fish Management ----
# ---- Fish Management ----
@login_required
@user_passes_test(admin_required)
def manage_fish(request):
    from inventory.models import FishCategory  # ensure this model exists

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        category_id = request.POST.get("category")
        image = request.FILES.get("image")

        # ✅ Save fish properly
        if name and price and stock and category_id:
            category = FishCategory.objects.get(id=category_id)
            FishItem.objects.create(
                category=category,
                name=name,
                price_per_kg=price,
                stock=stock,
                image=image,
            )
            return redirect("manage_fish")

    fish_list = FishItem.objects.all()
    categories = FishCategory.objects.all()

    return render(
        request,
        "adminpanel/fish_management.html",
        {"fish_list": fish_list, "categories": categories},
    )


@login_required
@user_passes_test(admin_required)
def add_fish(request):
    from inventory.models import FishCategory
    from django.contrib import messages
    
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        category_id = request.POST.get("category")
        image = request.FILES.get("image")

        if name and price and stock and category_id:
            try:
                category = FishCategory.objects.get(id=category_id)
                FishItem.objects.create(
                    category=category,
                    name=name,
                    price_per_kg=float(price),
                    stock=float(stock),
                    image=image,
                )
                messages.success(request, f'Fish "{name}" added successfully')
                return redirect("manage_fish")
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Please fill all required fields')
    
    categories = FishCategory.objects.all()
    return render(request, "adminpanel/add_fish.html", {"categories": categories})


@login_required
@user_passes_test(admin_required)
def edit_fish(request, fish_id):
    from inventory.models import FishCategory
    from django.contrib import messages
    
    fish = get_object_or_404(FishItem, id=fish_id)
    
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        category_id = request.POST.get("category")
        image = request.FILES.get("image")

        if name and price and stock and category_id:
            try:
                category = FishCategory.objects.get(id=category_id)
                fish.name = name
                fish.price_per_kg = float(price)
                fish.stock = float(stock)
                fish.category = category
                if image:
                    fish.image = image
                fish.save()
                messages.success(request, f'Fish "{name}" updated successfully')
                return redirect("manage_fish")
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Please fill all required fields')
    
    categories = FishCategory.objects.all()
    return render(request, "adminpanel/edit_fish.html", {"fish": fish, "categories": categories})


@login_required
@user_passes_test(admin_required)
def remove_fish(request, fish_id):
    fish = get_object_or_404(FishItem, id=fish_id)
    fish_name = fish.name
    fish.delete()
    from django.contrib import messages
    messages.success(request, f'Fish "{fish_name}" removed successfully')
    return redirect("manage_fish")


@login_required
@user_passes_test(admin_required)
def manage_categories(request):
    from inventory.models import FishCategory
    categories = FishCategory.objects.all()
    return render(request, "adminpanel/categories.html", {"categories": categories})


@login_required
@user_passes_test(admin_required)
def add_category(request):
    from inventory.models import FishCategory
    from django.contrib import messages
    
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            try:
                FishCategory.objects.create(name=name)
                messages.success(request, f'Category "{name}" added successfully')
                return redirect("manage_categories")
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Category name is required')
    
    return render(request, "adminpanel/add_category.html")


@login_required
@user_passes_test(admin_required)
def remove_category(request, category_id):
    from inventory.models import FishCategory
    from django.contrib import messages
    
    category = get_object_or_404(FishCategory, id=category_id)
    category_name = category.name
    category.delete()
    messages.success(request, f'Category "{category_name}" removed successfully')
    return redirect("manage_categories")




# ---- Shipping Management ----
@login_required
@user_passes_test(admin_required)
def shipping_handling(request):
    orders = Order.objects.all().order_by('-date')
    return render(request, "adminpanel/shipping.html", {"orders": orders})


@login_required
@user_passes_test(admin_required)
def update_order_status(request, order_id):
    from django.contrib import messages
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {new_status}')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect("shipping_handling")


# ---- Complaints ----
@login_required
@user_passes_test(admin_required)
def view_complaints(request):
    complaints = Complaint.objects.all().order_by('-id')
    return render(request, "adminpanel/complaints.html", {"complaints": complaints})


@login_required
@user_passes_test(admin_required)
def reply_to_complaint(request, complaint_id):
    from django.contrib import messages
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == "POST":
        reply = request.POST.get("admin_reply")
        status = request.POST.get("status", "Resolved")
        
        if reply:
            complaint.admin_reply = reply
            complaint.status = status
            complaint.save()
            messages.success(request, 'Reply sent successfully')
            return redirect("view_complaints")
        else:
            messages.error(request, 'Reply cannot be empty')
    
    return render(request, "adminpanel/reply_complaint.html", {"complaint": complaint})


# ---- Reports ----
@login_required
@user_passes_test(admin_required)
def reports(request):
    from fishermen.models import DailyCatch
    
    total_sales = Order.objects.aggregate(total=Sum("total_amount"))["total"] or 0
    
    # Get fish sales from DailyCatch
    from django.db.models import Sum, Count
    fish_sales = DailyCatch.objects.values('fish_type').annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')
    
    return render(
        request,
        "adminpanel/reports.html",
        {"total_sales": total_sales, "fish_sales": fish_sales},
    )
