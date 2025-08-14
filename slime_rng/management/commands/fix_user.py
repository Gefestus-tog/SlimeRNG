from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from slime_rng.models import SlimeType, Collection, CraftRecipe, PlayerInventory, PlayerCollection, PlayerCraft

User = get_user_model()

class Command(BaseCommand):
    help = 'Fix user profile and permissions'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to fix')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"Found user: {user.username}")
            
            # Make sure user is staff and superuser
            if not user.is_staff or not user.is_superuser:
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(self.style.SUCCESS("✅ Fixed user permissions"))
            
            # Check and create PlayerCollections
            collections_count = PlayerCollection.objects.filter(player=user).count()
            total_collections = Collection.objects.count()
            self.stdout.write(f"PlayerCollections: {collections_count}/{total_collections}")
            
            if collections_count < total_collections:
                self.stdout.write("Creating missing PlayerCollections...")
                all_collections = Collection.objects.all()
                created = 0
                for collection in all_collections:
                    pc, created_new = PlayerCollection.objects.get_or_create(
                        player=user, 
                        collection=collection
                    )
                    if created_new:
                        created += 1
                        self.stdout.write(f"  ✅ Created: {collection.name}")
                
                self.stdout.write(self.style.SUCCESS(f"Created {created} new PlayerCollections"))
            
            # Check and create PlayerInventory
            inventory_count = PlayerInventory.objects.filter(player=user).count()
            total_slimes = SlimeType.objects.count()
            self.stdout.write(f"PlayerInventory: {inventory_count}/{total_slimes}")
            
            if inventory_count < total_slimes:
                self.stdout.write("Creating missing PlayerInventory...")
                all_slimes = SlimeType.objects.all()
                created = 0
                for slime in all_slimes:
                    inv, created_new = PlayerInventory.objects.get_or_create(
                        player=user, 
                        slime_type=slime,
                        defaults={'amount': slime.base_amount}
                    )
                    if created_new:
                        created += 1
                
                self.stdout.write(self.style.SUCCESS(f"Created {created} new PlayerInventory entries"))
            
            # Check and create PlayerCrafts
            crafts_count = PlayerCraft.objects.filter(player=user).count()
            total_recipes = CraftRecipe.objects.count()
            self.stdout.write(f"PlayerCrafts: {crafts_count}/{total_recipes}")
            
            if crafts_count < total_recipes:
                self.stdout.write("Creating missing PlayerCrafts...")
                all_recipes = CraftRecipe.objects.all()
                created = 0
                for recipe in all_recipes:
                    craft, created_new = PlayerCraft.objects.get_or_create(
                        player=user,
                        recipe=recipe
                    )
                    if created_new:
                        created += 1
                
                self.stdout.write(self.style.SUCCESS(f"Created {created} new PlayerCraft entries"))
            
            self.stdout.write(self.style.SUCCESS(f"✅ User {username} profile is complete!"))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ User {username} not found!"))