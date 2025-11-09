# FishNet - Quick Start Guide

## Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create Sample Categories (Optional)
```bash
python setup.py
```

### 4. Start the Server
```bash
python manage.py runserver
```

### 5. Access the Application
Open your browser and go to: `http://127.0.0.1:8000/`

## Default Login Credentials

### Admin Account
- **URL**: `http://127.0.0.1:8000/login/`
- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full admin dashboard with all management features

### Staff Account
- **Username**: `staff`
- **Password**: `staff123`
- **Access**: Staff dashboard to view orders

### Fisherman Account
- **Username**: `fisherman`
- **Password**: `fish123`
- **Note**: A fisherman profile must be created by admin first

## First Steps After Login

### As Admin:
1. Go to **Fish Inventory** to add fish categories and items
2. Go to **Fishermen** to view/manage registered fishermen
3. Go to **Users** to view/manage customers
4. Go to **Reports** to view sales statistics

### As Customer:
1. Browse available fish at `/inventory/`
2. View fish details, prices, and stock

### As Fisherman:
1. View your dashboard
2. Add daily catches
3. File complaints if needed

## Adding Fish Items (Admin)

1. Login as admin
2. Go to **Fish Inventory** from dashboard
3. Make sure you have categories created (run `python setup.py` if needed)
4. Fill in the form:
   - Fish Name
   - Category (select from dropdown)
   - Price per kg
   - Stock (kg)
   - Image (optional)
5. Click **Add Fish**

## Creating a Fisherman Profile (Admin)

1. Login as admin
2. Create a user account first (or use existing)
3. Go to Django admin panel: `http://127.0.0.1:8000/admin/`
4. Navigate to **Fishermen** > **Fisherman profiles**
5. Add new fisherman profile and link to user

## Troubleshooting

### Images not showing?
- Ensure `media/` folder exists in project root
- Check that `MEDIA_URL` and `MEDIA_ROOT` are set in `settings.py`

### Migration errors?
- Delete `db.sqlite3` and run migrations again
- Or run: `python manage.py makemigrations` then `python manage.py migrate`

### Can't login?
- Make sure you've run migrations
- Try creating a superuser: `python manage.py createsuperuser`

## Need Help?

Refer to the full [README.md](README.md) for detailed documentation.

