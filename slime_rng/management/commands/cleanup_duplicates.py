from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from slime_rng.models import CraftRecipe, PlayerCraft, CraftIngredient

User = get_user_model()

class Command(BaseCommand):
    help = 'Clean up duplicate craft recipes and fix user permissions'

    def handle(self, *args, **options):
        self.stdout.write("🧹 Cleaning up duplicate craft recipes...")
        
        # List of old recipe names to remove (from migration 0006)
        old_recipe_names = [
            "Амулет удачи",  # The old one with rareChanceBoost
            "Амулет скорости",  # The old one with spinCooldown
        ]
        
        # Find and remove old recipes
        for recipe_name in old_recipe_names:
            old_recipes = CraftRecipe.objects.filter(
                name=recipe_name,
                effect_type__in=['rareChanceBoost', 'spinCooldown']  # Old effect types
            )
            
            for recipe in old_recipes:
                self.stdout.write(f"🗑️  Removing old recipe: {recipe.name} (ID: {recipe.id}, type: {recipe.effect_type})")
                
                # Remove associated PlayerCraft entries
                PlayerCraft.objects.filter(recipe=recipe).delete()
                
                # Remove associated ingredients
                CraftIngredient.objects.filter(recipe=recipe).delete()
                
                # Remove the recipe
                recipe.delete()
        
        self.stdout.write("✅ Duplicate recipes cleaned up!")
        
        # Now fix the Gefest user
        self.stdout.write("🔧 Fixing user permissions and profile...")
        
        try:
            user = User.objects.get(username='Gefest')
            self.stdout.write(f"Found user: {user.username}")
            
            # Check current permissions
            self.stdout.write(f"Current permissions - is_staff: {user.is_staff}, is_superuser: {user.is_superuser}, is_active: {user.is_active}")
            
            # Fix permissions
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            
            self.stdout.write("✅ Updated user permissions")
            self.stdout.write(f"New permissions - is_staff: {user.is_staff}, is_superuser: {user.is_superuser}, is_active: {user.is_active}")
            
            # Recreate PlayerCraft entries for current recipes
            current_recipes = CraftRecipe.objects.all()
            self.stdout.write(f"Current recipes count: {current_recipes.count()}")
            
            for recipe in current_recipes:
                craft, created = PlayerCraft.objects.get_or_create(
                    player=user,
                    recipe=recipe
                )
                if created:
                    self.stdout.write(f"  ✅ Created PlayerCraft for: {recipe.name}")
            
            # Verify final counts
            from slime_rng.models import PlayerCollection, PlayerInventory
            collections_count = PlayerCollection.objects.filter(player=user).count()
            inventory_count = PlayerInventory.objects.filter(player=user).count()
            crafts_count = PlayerCraft.objects.filter(player=user).count()
            
            self.stdout.write(f"📊 Final counts:")
            self.stdout.write(f"  Collections: {collections_count}")
            self.stdout.write(f"  Inventory: {inventory_count}")
            self.stdout.write(f"  Crafts: {crafts_count}")
            
            self.stdout.write(self.style.SUCCESS("🎉 All cleanup and fixes completed!"))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ User 'Gefest' not found!"))