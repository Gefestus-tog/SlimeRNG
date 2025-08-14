#!/usr/bin/env sh
set -e

# Wait for database to be ready with simple sleep
echo "Waiting for database..."
sleep 10

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Populate initial data
python manage.py populate_slimes

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model
from slime_rng.models import SlimeType, Collection, CraftRecipe, PlayerInventory, PlayerCollection, PlayerCraft
User = get_user_model()
if not User.objects.filter(username='Gefest').exists():
    user = User.objects.create_superuser('Gefest', 'oppoosite23@gmail.com', 'X2120558Xc')
    
    # Create inventory for all slime types
    for slime_type in SlimeType.objects.all():
        PlayerInventory.objects.create(player=user, slime_type=slime_type, amount=slime_type.base_amount)
    
    # Create collections for user
    for collection in Collection.objects.all():
        PlayerCollection.objects.create(player=user, collection=collection)
    
    # Create crafts for user
    for recipe in CraftRecipe.objects.all():
        PlayerCraft.objects.create(player=user, recipe=recipe)
    
    print('Superuser created with complete profile: Gefest')
else:
    print('Superuser already exists')
"

exec "$@"


