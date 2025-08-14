from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model, authenticate
from slime_rng.models import PlayerCollection, PlayerInventory, PlayerCraft, Collection

User = get_user_model()

class Command(BaseCommand):
    help = 'Debug user issues'

    def handle(self, *args, **options):
        username = 'Gefest'
        password = 'X2120558Xc'
        
        self.stdout.write("🔍 Debugging user issues...")
        
        # Check if user exists
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"✅ User exists: {user.username}")
            
            # Check user attributes
            self.stdout.write(f"📊 User details:")
            self.stdout.write(f"  - ID: {user.id}")
            self.stdout.write(f"  - Username: {user.username}")
            self.stdout.write(f"  - Email: {user.email}")
            self.stdout.write(f"  - is_active: {user.is_active}")
            self.stdout.write(f"  - is_staff: {user.is_staff}")
            self.stdout.write(f"  - is_superuser: {user.is_superuser}")
            self.stdout.write(f"  - date_joined: {user.date_joined}")
            self.stdout.write(f"  - last_login: {user.last_login}")
            self.stdout.write(f"  - has_usable_password: {user.has_usable_password()}")
            
            # Test authentication
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                self.stdout.write("✅ Authentication successful")
            else:
                self.stdout.write("❌ Authentication failed")
                
                # Try to set password again
                user.set_password(password)
                user.save()
                self.stdout.write("🔄 Reset password, trying again...")
                
                auth_user = authenticate(username=username, password=password)
                if auth_user:
                    self.stdout.write("✅ Authentication now works!")
                else:
                    self.stdout.write("❌ Authentication still failing")
            
            # Check related objects
            collections_count = PlayerCollection.objects.filter(player=user).count()
            inventory_count = PlayerInventory.objects.filter(player=user).count()
            crafts_count = PlayerCraft.objects.filter(player=user).count()
            
            self.stdout.write(f"📦 Related objects:")
            self.stdout.write(f"  - PlayerCollections: {collections_count}")
            self.stdout.write(f"  - PlayerInventory: {inventory_count}")
            self.stdout.write(f"  - PlayerCrafts: {crafts_count}")
            
            # Check collections in detail
            if collections_count > 0:
                self.stdout.write("📋 Collections detail:")
                collections = PlayerCollection.objects.filter(player=user)
                for pc in collections:
                    self.stdout.write(f"  - {pc.collection.name}: completed={pc.completed}")
            
            # Check total collections available
            total_collections = Collection.objects.count()
            self.stdout.write(f"🎯 Total collections in system: {total_collections}")
            
        except User.DoesNotExist:
            self.stdout.write(f"❌ User {username} not found!")
            
            # List all users
            all_users = User.objects.all()
            self.stdout.write(f"👥 All users in system: {all_users.count()}")
            for u in all_users:
                self.stdout.write(f"  - {u.username} (staff: {u.is_staff}, super: {u.is_superuser})")
        
        self.stdout.write("🏁 Debug complete!")