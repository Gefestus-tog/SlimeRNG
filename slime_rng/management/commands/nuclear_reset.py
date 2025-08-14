from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from slime_rng.models import PlayerCollection, Collection

User = get_user_model()

class Command(BaseCommand):
    help = 'Nuclear option - just fix the collections issue'

    def handle(self, *args, **options):
        self.stdout.write("💥 NUCLEAR RESET - Collections Fix Only...")
        
        try:
            # Get the user
            user = User.objects.get(username='Gefest')
            self.stdout.write(f"Found user: {user.username}")
            
            # Delete ALL PlayerCollections for this user
            deleted_count = PlayerCollection.objects.filter(player=user).delete()[0]
            self.stdout.write(f"Deleted {deleted_count} old PlayerCollections")
            
            # Get all collections
            all_collections = Collection.objects.all()
            self.stdout.write(f"Found {all_collections.count()} collections in system")
            
            # Create fresh PlayerCollections
            created_count = 0
            for collection in all_collections:
                pc = PlayerCollection.objects.create(
                    player=user,
                    collection=collection,
                    completed=False,
                    claimed=False
                )
                created_count += 1
                self.stdout.write(f"✅ Created PlayerCollection: {collection.name}")
            
            self.stdout.write(f"🎯 Created {created_count} new PlayerCollections")
            
            # Test serialization
            from slime_rng.serializers import PlayerCollectionSerializer
            collections_qs = PlayerCollection.objects.filter(player=user)
            serializer = PlayerCollectionSerializer(collections_qs, many=True)
            
            self.stdout.write(f"📊 Verification:")
            self.stdout.write(f"  - PlayerCollections in DB: {collections_qs.count()}")
            self.stdout.write(f"  - Serializer data length: {len(serializer.data)}")
            
            if serializer.data:
                self.stdout.write(f"  - First collection: {serializer.data[0]['collection']['name']}")
            
            self.stdout.write(self.style.SUCCESS("🎉 Collections should now work!"))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ User 'Gefest' not found!"))