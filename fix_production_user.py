#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from slime_rng.models import SlimeType, Collection, CraftRecipe, PlayerInventory, PlayerCollection, PlayerCraft

User = get_user_model()

def fix_user(username='Gefest'):
    try:
        user = User.objects.get(username=username)
        print(f"Found user: {user.username}")
        print(f"Is staff: {user.is_staff}")
        print(f"Is superuser: {user.is_superuser}")
        
        # Make sure user is staff and superuser
        if not user.is_staff or not user.is_superuser:
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print("✅ Fixed user permissions")
        
        # Check PlayerCollection count
        collections_count = PlayerCollection.objects.filter(player=user).count()
        print(f"PlayerCollections: {collections_count}")
        
        if collections_count == 0:
            print("Creating PlayerCollections...")
            all_collections = Collection.objects.all()
            for collection in all_collections:
                PlayerCollection.objects.create(player=user, collection=collection)
                print(f"  ✅ Created: {collection.name}")
        
        # Check PlayerInventory count  
        inventory_count = PlayerInventory.objects.filter(player=user).count()
        print(f"PlayerInventory: {inventory_count}")
        
        if inventory_count == 0:
            print("Creating PlayerInventory...")
            all_slimes = SlimeType.objects.all()
            for slime in all_slimes:
                PlayerInventory.objects.create(player=user, slime_type=slime, amount=slime.base_amount)
                print(f"  ✅ Created inventory for: {slime.name}")
        
        # Check PlayerCraft count
        crafts_count = PlayerCraft.objects.filter(player=user).count()
        print(f"PlayerCrafts: {crafts_count}")
        
        print(f"\n✅ User {username} is ready!")
        return True
        
    except User.DoesNotExist:
        print(f"❌ User {username} not found!")
        return False

if __name__ == "__main__":
    fix_user()