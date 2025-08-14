from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from slime_rng.models import SlimeType, Collection, CraftRecipe, PlayerInventory, PlayerCollection, PlayerCraft

User = get_user_model()

class Command(BaseCommand):
    help = 'Force fix admin user and create complete profile'

    def handle(self, *args, **options):
        username = 'Gefest'
        password = 'X2120558Xc'
        email = 'oppoosite23@gmail.com'
        
        self.stdout.write("🔧 Force fixing admin user...")
        
        # Delete existing user if exists (to start fresh)
        try:
            existing_user = User.objects.get(username=username)
            self.stdout.write(f"Found existing user {username}, deleting to recreate...")
            existing_user.delete()
        except User.DoesNotExist:
            self.stdout.write(f"No existing user {username} found")
        
        # Create fresh superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(f"✅ Created fresh superuser: {username}")
        
        # Verify user settings
        user.refresh_from_db()
        self.stdout.write(f"User verification:")
        self.stdout.write(f"  - username: {user.username}")
        self.stdout.write(f"  - email: {user.email}")
        self.stdout.write(f"  - is_active: {user.is_active}")
        self.stdout.write(f"  - is_staff: {user.is_staff}")
        self.stdout.write(f"  - is_superuser: {user.is_superuser}")
        self.stdout.write(f"  - has_usable_password: {user.has_usable_password()}")
        
        # Test password
        from django.contrib.auth import authenticate
        auth_user = authenticate(username=username, password=password)
        if auth_user:
            self.stdout.write("✅ Password authentication works!")
        else:
            self.stdout.write("❌ Password authentication failed!")
        
        # Create complete profile
        self.stdout.write("🎮 Creating complete game profile...")
        
        # Create PlayerInventory for all slime types
        all_slimes = SlimeType.objects.all()
        self.stdout.write(f"Creating inventory for {all_slimes.count()} slime types...")
        for slime in all_slimes:
            PlayerInventory.objects.create(
                player=user,
                slime_type=slime,
                amount=slime.base_amount
            )
        
        # Create PlayerCollection for all collections
        all_collections = Collection.objects.all()
        self.stdout.write(f"Creating collections for {all_collections.count()} collections...")
        for collection in all_collections:
            PlayerCollection.objects.create(
                player=user,
                collection=collection,
                completed=False,
                claimed=False
            )
            self.stdout.write(f"  ✅ Created collection: {collection.name}")
        
        # Create PlayerCraft for all recipes
        all_recipes = CraftRecipe.objects.all()
        self.stdout.write(f"Creating crafts for {all_recipes.count()} recipes...")
        for recipe in all_recipes:
            PlayerCraft.objects.create(
                player=user,
                recipe=recipe,
                is_completed=False
            )
        
        # Final verification
        inventory_count = PlayerInventory.objects.filter(player=user).count()
        collections_count = PlayerCollection.objects.filter(player=user).count()
        crafts_count = PlayerCraft.objects.filter(player=user).count()
        
        self.stdout.write(f"📊 Final profile:")
        self.stdout.write(f"  - Inventory items: {inventory_count}")
        self.stdout.write(f"  - Collections: {collections_count}")
        self.stdout.write(f"  - Crafts: {crafts_count}")
        
        # Test API serialization
        from slime_rng.serializers import PlayerCollectionSerializer
        collections_qs = PlayerCollection.objects.filter(player=user)
        serializer = PlayerCollectionSerializer(collections_qs, many=True)
        self.stdout.write(f"  - Collections serialize correctly: {len(serializer.data) > 0}")
        
        self.stdout.write(self.style.SUCCESS("🎉 Complete admin setup finished!"))
        self.stdout.write(f"👤 Login with: {username} / {password}")
        self.stdout.write("🔗 Admin URL: /admin/")
        self.stdout.write("📡 API should now return collections data")