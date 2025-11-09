from django.shortcuts import render, redirect
from .models import DailyCatch, Complaint, FishermanProfile
from .forms import FishermanRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def fisherman_registration(request):
    """Fisherman registration form with verification details"""
    if request.user.role != 'fisherman':
        messages.error(request, 'Only fishermen can access this page.')
        return redirect('home')
    
    # Check if profile already exists
    try:
        profile = request.user.fishermanprofile
        if profile.status == 'Approved':
            messages.info(request, 'Your profile is already approved.')
            return redirect('fisherman_dashboard')
        else:
            messages.info(request, 'Your profile is pending approval. You can update your details.')
    except FishermanProfile.DoesNotExist:
        profile = None
    
    if request.method == 'POST':
        form = FishermanRegistrationForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            fisherman_profile = form.save(commit=False)
            fisherman_profile.user = request.user
            fisherman_profile.status = 'Pending'
            fisherman_profile.save()
            messages.success(request, 'Registration submitted! Your profile will be reviewed by admin.')
            return redirect('fisherman_dashboard')
    else:
        form = FishermanRegistrationForm(instance=profile)
    
    return render(request, 'fishermen/registration.html', {'form': form, 'profile': profile})


@login_required
def fisherman_dashboard(request):
    if request.user.role != 'fisherman':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Check if profile exists
    try:
        profile = request.user.fishermanprofile
    except FishermanProfile.DoesNotExist:
        messages.warning(request, 'Please complete your fisherman registration first.')
        return redirect('fisherman_registration')
    
    catches = DailyCatch.objects.filter(fisherman=profile).order_by('-date')
    complaints = Complaint.objects.filter(fisherman=profile).order_by('-id')
    return render(request, 'fishermen/dashboard.html', {
        'catches': catches, 
        'complaints': complaints, 
        'profile': profile
    })


@login_required
def add_catch(request):
    if request.user.role != 'fisherman':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        profile = request.user.fishermanprofile
    except FishermanProfile.DoesNotExist:
        messages.warning(request, 'Please complete your registration first.')
        return redirect('fisherman_registration')
    
    if profile.status != 'Approved':
        messages.warning(request, 'Your profile is pending approval. You cannot add catches yet.')
        return redirect('fisherman_dashboard')

    if request.method == 'POST':
        fish = request.POST.get('fish_type')
        qty = float(request.POST.get('quantity', '0'))
        price = float(request.POST.get('price', '0'))

        if fish and qty > 0 and price > 0:
            DailyCatch.objects.create(
                fisherman=profile,
                fish_type=fish,
                quantity=qty,
                price_per_kg=price
            )
            messages.success(request, 'Daily catch added')
            return redirect('fisherman_dashboard')
        else:
            messages.error(request, 'Please fill all fields correctly.')

    return render(request, 'fishermen/add_catch.html')


@login_required
def file_complaint(request):
    if request.user.role != 'fisherman':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    try:
        profile = request.user.fishermanprofile
    except FishermanProfile.DoesNotExist:
        messages.warning(request, 'Please complete your registration first.')
        return redirect('fisherman_registration')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title and description:
            Complaint.objects.create(
                fisherman=profile,
                title=title,
                description=description,
                status='Pending'
            )
            messages.success(request, 'Complaint filed successfully')
            return redirect('fisherman_dashboard')
        else:
            messages.error(request, 'Please fill all fields')

    return render(request, 'fishermen/file_complaint.html')
