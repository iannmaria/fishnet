from django.shortcuts import render, get_object_or_404
from .models import FishItem

# ✅ Display all available fish to customers
def inventory_list(request):
    fish_items = FishItem.objects.all().order_by('name')
    return render(request, 'inventory/list.html', {'fish_items': fish_items})


# ✅ Optional: Single fish detail page (if user clicks “View Details”)
def fish_detail(request, fish_id):
    fish = get_object_or_404(FishItem, id=fish_id)
    return render(request, 'inventory/fish_detail.html', {'fish': fish})
