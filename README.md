# FishNet - Django Web Application

FishNet is a Django-based web application designed to connect fishermen, customers, and administrators on a single digital marketplace. It allows fishermen to register and sell fish, customers to view and buy available fish, and admins to manage users, fishermen, staff, fish inventory, complaints, and reports.

## Features

### Admin Functions
- Secure login (only superusers can access the admin dashboard)
- Dashboard showing total fishermen, customers, staff, and fish count
- Manage fishermen: View / Remove fishermen
- Manage customers: View / Remove customers
- Manage staff: View / Edit staff and assign special functions
- Manage fish: Add / Remove fish with images, category, price, and stock
- Handle shipping & orders
- View complaints from both customers and fishermen
- Generate sales and inventory reports

### Customer Functions
- View available fish with image, price, and stock
- Logout securely
- Future scope: Add to cart, buy fish, order tracking

### Fisherman Functions
- Register and manage their profile
- File complaints
- View daily catches
- Future scope: Add fish to marketplace (to be approved by admin)

## Project Structure

```
fishnet/
├── fishnet/              # Project configuration files
│   ├── settings.py       # Main project settings
│   ├── urls.py           # Global URL routing
│   └── wsgi.py           # Entry point for deployment
├── adminpanel/           # Custom admin dashboard module
│   ├── templates/adminpanel/
│   │   ├── dashboard.html
│   │   ├── fisherman_list.html
│   │   ├── user_list.html
│   │   ├── staff_list.html
│   │   ├── fish_management.html
│   │   ├── complaints.html
│   │   ├── reports.html
│   │   └── shipping.html
│   └── views.py          # Admin-related functions
├── inventory/            # Handles all fish-related data
│   ├── models.py         # FishItem and FishCategory models
│   ├── views.py          # Logic to fetch/display fish data
│   └── templates/inventory/
│       └── list.html     # Displays fish to customers
├── fishermen/            # Fishermen management module
│   ├── models.py         # FishermanProfile and Complaint models
│   └── views.py          # Logic for fishermen actions
├── users/                # Handles authentication & user management
│   ├── models.py         # CustomUser model
│   └── views.py          # Login, register, and logout logic
├── orders/               # Handles orders and shipping
│   └── models.py         # Order model
├── templates/
│   └── base.html         # Common layout for all pages
└── manage.py             # Main entry point for Django commands
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Navigate to Project Directory
```bash
cd fishnet-django
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

Alternatively, you can use the special login credentials:
- **Admin**: username: `admin`, password: `admin123`
- **Staff**: username: `staff`, password: `staff123`
- **Fisherman**: username: `fisherman`, password: `fish123`

### Step 6: Create Sample Data (Optional)
If you want to populate the database with sample fish categories:
```bash
python manage.py shell
```

Then in the shell:
```python
from inventory.models import FishCategory

# Create sample categories
FishCategory.objects.create(name="Freshwater")
FishCategory.objects.create(name="Saltwater")
FishCategory.objects.create(name="Shellfish")
FishCategory.objects.create(name="Crustaceans")
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### Admin Access
1. Navigate to `http://127.0.0.1:8000/`
2. Click "Login" or go to `http://127.0.0.1:8000/login/`
3. Login with admin credentials (username: `admin`, password: `admin123`)
4. You'll be redirected to the admin dashboard
5. From the dashboard, you can:
   - View and manage fishermen
   - View and manage customers
   - View and manage staff
   - Add/remove fish items
   - View orders and shipping
   - View complaints
   - Generate reports

### Customer Access
1. Sign up for a new account at `http://127.0.0.1:8000/signup/`
2. Login with your credentials
3. Browse available fish at `http://127.0.0.1:8000/inventory/`

### Fisherman Access
1. Login with fisherman credentials (username: `fisherman`, password: `fish123`)
2. Note: A fisherman profile must be created by admin first
3. View dashboard, add catches, and file complaints

## Default Login Credentials

- **Admin**: 
  - Username: `admin`
  - Password: `admin123`
  
- **Staff**: 
  - Username: `staff`
  - Password: `staff123`
  
- **Fisherman**: 
  - Username: `fisherman`
  - Password: `fish123`

## Media Files

Uploaded images (fish photos) are stored in the `media/` directory. Make sure this directory exists and has proper write permissions.

## Database

The project uses SQLite by default (for development). The database file is `db.sqlite3` in the project root.

## Troubleshooting

### Issue: Images not displaying
- Make sure `MEDIA_URL` and `MEDIA_ROOT` are properly configured in `settings.py`
- Ensure the `media/` directory exists
- Check that `DEBUG = True` in settings for development

### Issue: Migration errors
- Delete `db.sqlite3` and migration files in each app's `migrations/` folder (except `__init__.py`)
- Run `python manage.py makemigrations` again
- Run `python manage.py migrate`

### Issue: Static files not loading
- Run `python manage.py collectstatic` (for production)
- Ensure `STATICFILES_DIRS` is configured in `settings.py`

## Future Enhancements

- Add to cart functionality for customers
- Order placement and tracking
- Payment integration
- Fisherman can add fish to marketplace (pending admin approval)
- Email notifications
- Advanced reporting and analytics
- Mobile responsive improvements

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please contact the development team.

---

**Note**: This is a development version. For production deployment, ensure to:
- Set `DEBUG = False`
- Configure proper database (PostgreSQL recommended)
- Set up proper static file serving
- Configure security settings
- Use environment variables for sensitive data

