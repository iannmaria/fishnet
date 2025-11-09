"""
Quick setup script to initialize the FishNet project.
Run this after installing dependencies to set up initial data.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fishnet.settings')
django.setup()

from inventory.models import FishCategory

def setup_categories():
    """Create default fish categories if they don't exist"""
    categories = [
        "Freshwater",
        "Saltwater",
        "Shellfish",
        "Crustaceans",
        "Other"
    ]
    
    created_count = 0
    for cat_name in categories:
        category, created = FishCategory.objects.get_or_create(name=cat_name)
        if created:
            created_count += 1
            print(f"✓ Created category: {cat_name}")
        else:
            print(f"  Category already exists: {cat_name}")
    
    print(f"\n✓ Setup complete! Created {created_count} new categories.")

if __name__ == '__main__':
    print("Setting up FishNet...")
    setup_categories()
    print("\nYou can now run: python manage.py runserver")

