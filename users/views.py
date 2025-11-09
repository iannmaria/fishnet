from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import CustomUser


# ✅ Public home page
def home(request):
    # If logged-in user visits home, redirect them to their dashboard
    if request.user.is_authenticated:
        if request.user.role == "admin":
            return redirect('/adminpanel/dashboard/')
        elif request.user.role == "staff":
            return redirect('staff_dashboard')
        elif request.user.role == "fisherman":
            return redirect('fisherman_dashboard')
        else:
            return redirect('customer_dashboard')

    # Otherwise, show the public homepage
    return render(request, 'public_home.html')


# 🧑‍💻 Special login credentials
SPECIAL_LOGINS = {
    "admin_key": {"username": "admin", "password": "admin123", "role": "admin"},
    "staff_key": {"username": "staff", "password": "staff123", "role": "staff"},
    "fisher_key": {"username": "fisherman", "password": "fish123", "role": "fisherman"},
}


# ✅ Signup
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role', 'customer')
            user.role = role
            
            # Set staff permissions if staff
            if role == 'staff':
                user.is_staff = True
            else:
                user.is_staff = False
            
            user.save()
            
            # If fisherman, auto-login and redirect to registration
            if role == 'fisherman':
                from django.contrib import messages
                from django.contrib.auth import login
                login(request, user)
                messages.info(request, 'Please complete your fisherman profile registration.')
                return redirect('fisherman_registration')
            
            # For customer and staff, auto-login and redirect
            from django.contrib import messages
            from django.contrib.auth import login
            login(request, user)
            messages.success(request, 'Account created successfully!')
            
            # Redirect based on role
            if role == 'staff':
                return redirect('staff_dashboard')
            else:
                return redirect('customer_dashboard')
    else:
        form = SignupForm()
    return render(request, "users/signup.html", {"form": form})


# ✅ Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ✅ Handle special admin/staff/fisher keys
        for key, creds in SPECIAL_LOGINS.items():
            if username == creds['username'] and password == creds['password']:
                user, created = CustomUser.objects.get_or_create(
                    username=creds['username'],
                    defaults={"role": creds['role'], "email": f"{creds['role']}@fishnet.com"}
                )

                # ✅ Assign Django permissions based on role
                if creds['role'] == 'admin':
                    user.is_superuser = True
                    user.is_staff = True
                elif creds['role'] == 'staff':
                    user.is_staff = True
                    user.is_superuser = False
                else:
                    user.is_staff = False
                    user.is_superuser = False

                user.set_password(creds['password'])
                user.save()
                
                # ✅ Create fisherman profile if fisherman and doesn't exist (for special login only)
                if creds['role'] == 'fisherman':
                    from fishermen.models import FishermanProfile
                    FishermanProfile.objects.get_or_create(
                        user=user,
                        defaults={
                            'location': 'Not Set',
                            'license_id': f'DEMO-{user.id}',
                            'phone_number': '0000000000',
                            'address': 'Demo Address',
                            'status': 'Pending'
                        }
                    )
                
                login(request, user)

                # ✅ Redirect by role
                if creds['role'] == 'admin':
                    return redirect('/adminpanel/dashboard/')
                elif creds['role'] == 'staff':
                    return redirect('staff_dashboard')
                elif creds['role'] == 'fisherman':
                    return redirect('fisherman_dashboard')
                else:
                    return redirect('customer_dashboard')

        # ✅ Normal user login
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == "admin":
                return redirect('/adminpanel/dashboard/')
            elif user.role == "staff":
                return redirect("staff_dashboard")
            elif user.role == "fisherman":
                return redirect("fisherman_dashboard")
            else:
                return redirect("customer_dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


# ✅ Dashboards
@login_required
def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')


@login_required
def staff_dashboard(request):
    return render(request, 'users/staff_dashboard.html')


@login_required
def fisherman_dashboard(request):
    # Redirect to fishermen app dashboard
    return redirect('fisherman_dashboard')


@login_required
def customer_dashboard(request):
    return redirect('inventory_list')


# ✅ Logout function
def user_logout(request):
    logout(request)
    return redirect('home')  # Redirects back to homepage after logout
