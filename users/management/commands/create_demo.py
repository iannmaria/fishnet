from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from inventory.models import FishCategory, FishItem
from fishermen.models import FishermanProfile, DailyCatch


class Command(BaseCommand):
    help = 'Create demo users and sample data'

    def handle(self, *args, **options):
        User = get_user_model()

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin',
                'admin@example.com',
                'admin123',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user (admin/admin123)'))
        else:
            self.stdout.write('Admin exists')

        # Create fisherman user and demo data
        if not User.objects.filter(username='fisher1').exists():
            f1 = User.objects.create_user(
                'fisher1',
                'f1@example.com',
                'pass1234',
                role='fisherman'
            )
            profile = FishermanProfile.objects.create(
                user=f1,
                location='Coastal Village',
                license_id='LIC123',
                status='Approved'
            )
            DailyCatch.objects.create(
                fisherman=profile,
                fish_type='Rohu',
                quantity=30.0,
                price_per_kg=120.0
            )
            self.stdout.write(self.style.SUCCESS('Created fisherman user (fisher1)'))
        else:
            self.stdout.write('Fisherman user exists')

        # Create sample fish categories and items
        cat, _ = FishCategory.objects.get_or_create(name='Freshwater')
        FishItem.objects.get_or_create(category=cat, name='Rohu', price_per_kg=120.0, stock=200.0)
        FishItem.objects.get_or_create(category=cat, name='Catla', price_per_kg=150.0, stock=100.0)

        cat2, _ = FishCategory.objects.get_or_create(name='Saltwater')
        FishItem.objects.get_or_create(category=cat2, name='Pomfret', price_per_kg=400.0, stock=50.0)

        self.stdout.write(self.style.SUCCESS('Created fish items'))
