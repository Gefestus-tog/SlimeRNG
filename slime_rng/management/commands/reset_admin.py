from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Reset admin user password and permissions'

    def handle(self, *args, **options):
        username = 'Gefest'
        password = 'X2120558Xc'
        email = 'oppoosite23@gmail.com'
        
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"Found existing user: {user.username}")
            
            # Update password
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.email = email
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f"✅ Updated user {username}"))
            
        except User.DoesNotExist:
            # Create new superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Created new superuser: {username}"))
        
        # Verify settings
        self.stdout.write(f"Username: {user.username}")
        self.stdout.write(f"Email: {user.email}")
        self.stdout.write(f"is_staff: {user.is_staff}")
        self.stdout.write(f"is_superuser: {user.is_superuser}")
        self.stdout.write(f"is_active: {user.is_active}")
        self.stdout.write(f"Password set: {user.has_usable_password()}")
        
        self.stdout.write(self.style.SUCCESS("🎯 Admin login should now work!"))