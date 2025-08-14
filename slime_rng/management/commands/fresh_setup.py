from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from slime_rng.models import SlimeType, Collection, CollectionRequirement, CraftRecipe, CraftIngredient, PlayerInventory, PlayerCollection, PlayerCraft

User = get_user_model()

class Command(BaseCommand):
    help = 'Complete fresh setup from zero - clears and recreates everything'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Starting FRESH SETUP from zero...")
        
        with transaction.atomic():
            # STEP 1: Clear all existing data
            self.stdout.write("🧹 Step 1: Clearing existing data...")
            PlayerCraft.objects.all().delete()
            PlayerCollection.objects.all().delete()
            PlayerInventory.objects.all().delete()
            CraftIngredient.objects.all().delete()
            CraftRecipe.objects.all().delete()
            CollectionRequirement.objects.all().delete()
            Collection.objects.all().delete()
            SlimeType.objects.all().delete()
            User.objects.all().delete()
            self.stdout.write("✅ All data cleared!")
            
            # STEP 2: Create SlimeTypes
            self.stdout.write("🎮 Step 2: Creating SlimeTypes...")
            slimes_data = [
                {'name': 'Зелёный Слайм', 'image': 'slimes/green_slime.png', 'chance': '1/2', 'rarity': 'common', 'base_amount': 0},
                {'name': 'Синий Слайм', 'image': 'slimes/blue_slime.png', 'chance': '1/5', 'rarity': 'common', 'base_amount': 0},
                {'name': 'Красный Слайм', 'image': 'slimes/red_slime.png', 'chance': '1/10', 'rarity': 'common', 'base_amount': 0},
                {'name': 'Жёлтый Слайм', 'image': 'slimes/yellow_slime.png', 'chance': '1/20', 'rarity': 'common', 'base_amount': 0},
                {'name': 'Фиолетовый Слайм', 'image': 'slimes/purple_slime.png', 'chance': '1/50', 'rarity': 'common', 'base_amount': 0},
                {'name': 'Оранжевый Слайм', 'image': 'slimes/orange_slime.png', 'chance': '1/100', 'rarity': 'common', 'base_amount': 0},
                {'name': 'Болотный Слайм', 'image': 'slimes/swamp_slime.png', 'chance': '1/200', 'rarity': 'uncommon', 'base_amount': 0},
                {'name': 'Ледяной Слайм', 'image': 'slimes/ice_slime.png', 'chance': '1/300', 'rarity': 'uncommon', 'base_amount': 0},
                {'name': 'Огненный Слайм', 'image': 'slimes/fire_slime.png', 'chance': '1/400', 'rarity': 'uncommon', 'base_amount': 0},
                {'name': 'Электрический Слайм', 'image': 'slimes/electro_slime.png', 'chance': '1/500', 'rarity': 'uncommon', 'base_amount': 0},
                {'name': 'Каменный Слайм', 'image': 'slimes/rock_slime.png', 'chance': '1/750', 'rarity': 'uncommon', 'base_amount': 0},
                {'name': 'Водный Слайм', 'image': 'slimes/gidro_slime.png', 'chance': '1/1000', 'rarity': 'uncommon', 'base_amount': 0},
                {'name': 'Ведьма Слайм', 'image': 'slimes/witch_slime.png', 'chance': '1/2000', 'rarity': 'rare', 'base_amount': 0},
                {'name': 'Кристальный Слайм', 'image': 'slimes/crystal_slime.png', 'chance': '1/3000', 'rarity': 'rare', 'base_amount': 0},
                {'name': 'Лунный Слайм', 'image': 'slimes/moon_slime.png', 'chance': '1/5000', 'rarity': 'rare', 'base_amount': 0},
                {'name': 'Солнечный Слайм', 'image': 'slimes/sun_slime.png', 'chance': '1/7500', 'rarity': 'rare', 'base_amount': 0},
                {'name': 'Сладкий Слайм', 'image': 'slimes/candy_slime.png', 'chance': '1/10000', 'rarity': 'rare', 'base_amount': 0},
                {'name': 'Металлический Слайм', 'image': 'slimes/metal_slime.png', 'chance': '1/25000', 'rarity': 'epic', 'base_amount': 0},
                {'name': 'Серебряный Слайм', 'image': 'slimes/silver_slime.png', 'chance': '1/50000', 'rarity': 'epic', 'base_amount': 0},
                {'name': 'Золотой Слайм', 'image': 'slimes/golden_slime.png', 'chance': '1/75000', 'rarity': 'epic', 'base_amount': 0},
                {'name': 'Алмазный Слайм', 'image': 'slimes/diamond_slime.png', 'chance': '1/100000', 'rarity': 'epic', 'base_amount': 0},
                {'name': 'Драконий Слайм', 'image': 'slimes/dragon_slime.png', 'chance': '1/250000', 'rarity': 'legendary', 'base_amount': 0},
                {'name': 'Фениксовый Слайм', 'image': 'slimes/phoenix_slime.png', 'chance': '1/500000', 'rarity': 'legendary', 'base_amount': 0},
                {'name': 'Единорожный Слайм', 'image': 'slimes/unicorn_slime.png', 'chance': '1/750000', 'rarity': 'legendary', 'base_amount': 0},
                {'name': 'Космический Слайм', 'image': 'slimes/space_slime.png', 'chance': '1/1000000', 'rarity': 'legendary', 'base_amount': 0},
                {'name': 'Временной Слайм', 'image': 'slimes/time_slime.png', 'chance': '1/5000000', 'rarity': 'mythic', 'base_amount': 0},
                {'name': 'Портальный Слайм', 'image': 'slimes/portal_slime.png', 'chance': '1/10000000', 'rarity': 'mythic', 'base_amount': 0},
                {'name': 'Слайм Земля', 'image': 'slimes/earth_slime.png', 'chance': '1/50000000', 'rarity': 'mythic', 'base_amount': 0},
                {'name': 'Читер Слайм', 'image': 'slimes/cheater_slime.png', 'chance': '1/100000000', 'rarity': 'mythic', 'base_amount': 0},
                {'name': 'Божественный Слайм', 'image': 'slimes/god_slime.png', 'chance': '1/1000000000', 'rarity': 'divine', 'base_amount': 0},
                {'name': 'Первобытный Слайм', 'image': 'slimes/prehistoric_greenslime.png', 'chance': '1/5000000000', 'rarity': 'divine', 'base_amount': 0},
                {'name': 'Глитч Слайм', 'image': 'slimes/xuiznaet_slime.png', 'chance': '1/10000000000', 'rarity': 'divine', 'base_amount': 0},
            ]
            
            slime_objects = {}
            for slime_data in slimes_data:
                slime = SlimeType.objects.create(**slime_data)
                slime_objects[slime.name] = slime
            
            self.stdout.write(f"✅ Created {len(slimes_data)} SlimeTypes")
            
            # STEP 3: Create CraftRecipes
            self.stdout.write("🔨 Step 3: Creating CraftRecipes...")
            recipes_data = [
                {
                    'name': 'Амулет Слаймов',
                    'image': 'craft-items/slime_amulet.png',
                    'effect': 'Увеличивает удачу в 2.5 раза',
                    'effect_type': 'LuckBoost',
                    'effect_value': 2.5,
                    'ingredients': [('Зелёный Слайм', 5), ('Синий Слайм', 2), ('Электрический Слайм', 1)]
                },
                {
                    'name': 'Амулет Урожая',
                    'image': 'craft-items/harves_amulet.png',
                    'effect': 'Увеличивает получаемое количество слаймов на 1',
                    'effect_type': 'HarvestMultiplier',
                    'effect_value': 1,
                    'ingredients': [('Зелёный Слайм', 20), ('Жёлтый Слайм', 5), ('Золотой Слайм', 1)]
                },
                {
                    'name': 'Амулет Вечности',
                    'image': 'craft-items/infinity_amulet.png',
                    'effect': 'Увеличивает удачу в 10 раз',
                    'effect_type': 'LuckBoost',
                    'effect_value': 10,
                    'ingredients': [('Лунный Слайм', 1), ('Солнечный Слайм', 1), ('Временной Слайм', 1)]
                },
                {
                    'name': 'Амулет Изобилия',
                    'image': 'craft-items/abundance_amulet.png',
                    'effect': 'Получаешь на одного слайма больше',
                    'effect_type': 'HarvestMultiplier',
                    'effect_value': 1,
                    'ingredients': [('Фиолетовый Слайм', 10), ('Оранжевый Слайм', 5), ('Божественный Слайм', 1)]
                },
                {
                    'name': 'Амулет удачи',
                    'image': 'craft-items/Lucky_amulet.png',
                    'effect': 'Увеличивает шанс найти редкого слайма в 2 раза',
                    'effect_type': 'LuckBoost',
                    'effect_value': 2,
                    'ingredients': [('Зелёный Слайм', 10), ('Синий Слайм', 5)]
                },
                {
                    'name': 'Амулет скорости',
                    'image': 'craft-items/speed_amulet.png',
                    'effect': 'Уменьшает время восстановления спина на 20%',
                    'effect_type': 'SpinCooldown',
                    'effect_value': 0.8,
                    'ingredients': [('Красный Слайм', 10), ('Жёлтый Слайм', 5)]
                },
            ]
            
            recipe_objects = {}
            for recipe_data in recipes_data:
                recipe = CraftRecipe.objects.create(
                    name=recipe_data['name'],
                    image=recipe_data['image'],
                    effect=recipe_data['effect'],
                    effect_type=recipe_data['effect_type'],
                    effect_value=recipe_data['effect_value'],
                    created_by_default=True
                )
                
                # Add ingredients
                for slime_name, amount in recipe_data['ingredients']:
                    if slime_name in slime_objects:
                        CraftIngredient.objects.create(
                            recipe=recipe,
                            slime_type=slime_objects[slime_name],
                            amount=amount
                        )
                
                recipe_objects[recipe.name] = recipe
            
            self.stdout.write(f"✅ Created {len(recipes_data)} CraftRecipes")
            
            # STEP 4: Create Collections
            self.stdout.write("📋 Step 4: Creating Collections...")
            collections_data = [
                {
                    'name': 'Начальные слаймы',
                    'description': 'Собери всех основных слаймов',
                    'reward': 'Увеличивает удачу в 2 раза',
                    'effect_type': 'LuckBoost',
                    'effect_value': 2,
                    'requirements': [('Зелёный Слайм', 1), ('Синий Слайм', 1), ('Красный Слайм', 1), ('Жёлтый Слайм', 1)]
                },
                {
                    'name': 'Элементальные слаймы',
                    'description': 'Собери слаймов всех стихий',
                    'reward': 'Увеличивает получаемое количество слаймов на 1',
                    'effect_type': 'HarvestMultiplier',
                    'effect_value': 1,
                    'requirements': [('Ледяной Слайм', 1), ('Огненный Слайм', 1), ('Электрический Слайм', 1), ('Водный Слайм', 1)]
                },
                {
                    'name': 'Редкие экземпляры',
                    'description': 'Собери самых редких слаймов',
                    'reward': 'Уменьшает время восстановления спина на 30%',
                    'effect_type': 'SpinCooldown',
                    'effect_value': 0.7,
                    'requirements': [('Космический Слайм', 1), ('Временной Слайм', 1), ('Божественный Слайм', 1)]
                },
                {
                    'name': 'Все обычные',
                    'description': 'Собери по 10 экземпляров каждого обычного слайма',
                    'thumbnail': 'collections/common_slimes.png',
                    'reward': 'Дает х5 удачи',
                    'effect_type': 'LuckBoost',
                    'effect_value': 5,
                    'requirements': [('Зелёный Слайм', 10), ('Синий Слайм', 10), ('Красный Слайм', 10), ('Жёлтый Слайм', 10), ('Фиолетовый Слайм', 10), ('Оранжевый Слайм', 10)]
                },
                {
                    'name': 'Мифический набор',
                    'description': 'Собери всех мифических слаймов',
                    'reward': 'Удваивает удачу в 5 раз',
                    'effect_type': 'LuckBoost',
                    'effect_value': 5,
                    'requirements': [('Временной Слайм', 1), ('Портальный Слайм', 1), ('Слайм Земля', 1), ('Читер Слайм', 1)]
                },
            ]
            
            collection_objects = {}
            for collection_data in collections_data:
                collection = Collection.objects.create(
                    name=collection_data['name'],
                    description=collection_data['description'],
                    reward=collection_data['reward'],
                    effect_type=collection_data['effect_type'],
                    effect_value=collection_data['effect_value'],
                    thumbnail=collection_data.get('thumbnail')
                )
                
                # Add requirements
                for slime_name, amount in collection_data['requirements']:
                    if slime_name in slime_objects:
                        CollectionRequirement.objects.create(
                            collection=collection,
                            slime_type=slime_objects[slime_name],
                            amount=amount
                        )
                
                collection_objects[collection.name] = collection
            
            self.stdout.write(f"✅ Created {len(collections_data)} Collections")
            
            # STEP 5: Create Superuser with complete profile
            self.stdout.write("👤 Step 5: Creating Superuser...")
            user = User.objects.create_superuser(
                username='Gefest',
                email='oppoosite23@gmail.com',
                password='X2120558Xc'
            )
            
            # Create PlayerInventory
            for slime in slime_objects.values():
                PlayerInventory.objects.create(
                    player=user,
                    slime_type=slime,
                    amount=slime.base_amount
                )
            
            # Create PlayerCollections
            for collection in collection_objects.values():
                PlayerCollection.objects.create(
                    player=user,
                    collection=collection,
                    completed=False,
                    claimed=False
                )
            
            # Create PlayerCrafts
            for recipe in recipe_objects.values():
                PlayerCraft.objects.create(
                    player=user,
                    recipe=recipe,
                    is_completed=False
                )
            
            self.stdout.write("✅ Created Superuser with complete profile")
            
            # STEP 6: Final verification
            self.stdout.write("🔍 Step 6: Final verification...")
            
            # Test authentication
            auth_user = authenticate(username='Gefest', password='X2120558Xc')
            auth_ok = auth_user is not None
            
            # Count everything
            counts = {
                'slimes': SlimeType.objects.count(),
                'recipes': CraftRecipe.objects.count(),
                'collections': Collection.objects.count(),
                'users': User.objects.count(),
                'player_inventory': PlayerInventory.objects.filter(player=user).count(),
                'player_collections': PlayerCollection.objects.filter(player=user).count(),
                'player_crafts': PlayerCraft.objects.filter(player=user).count(),
            }
            
            self.stdout.write("📊 FINAL RESULTS:")
            self.stdout.write(f"  - SlimeTypes: {counts['slimes']}")
            self.stdout.write(f"  - CraftRecipes: {counts['recipes']}")
            self.stdout.write(f"  - Collections: {counts['collections']}")
            self.stdout.write(f"  - Users: {counts['users']}")
            self.stdout.write(f"  - PlayerInventory: {counts['player_inventory']}")
            self.stdout.write(f"  - PlayerCollections: {counts['player_collections']}")
            self.stdout.write(f"  - PlayerCrafts: {counts['player_crafts']}")
            self.stdout.write(f"  - Authentication: {'✅ WORKS' if auth_ok else '❌ FAILED'}")
            
        self.stdout.write(self.style.SUCCESS("🎉 FRESH SETUP COMPLETE!"))
        self.stdout.write("👤 Admin login: Gefest / X2120558Xc")
        self.stdout.write("🔗 Admin URL: /admin/")
        self.stdout.write("📡 API URL: /load/")