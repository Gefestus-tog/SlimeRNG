from django.core.management.base import BaseCommand
from slime_rng.models import SlimeType, Collection, CollectionRequirement, CraftRecipe, CraftIngredient


class Command(BaseCommand):
    help = 'Populate database with complete slime types, collections, and craft recipes'

    def handle(self, *args, **options):
        # Complete slimes data from the JSON
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

        created_count = 0
        for slime_data in slimes_data:
            slime, created = SlimeType.objects.get_or_create(
                name=slime_data['name'],
                defaults=slime_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created: {slime.name}")
            else:
                self.stdout.write(f"Already exists: {slime.name}")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} SlimeType objects')
        )

        # Create craft recipes
        self.create_craft_recipes()
        
        # Create collections
        self.create_collections()

    def create_craft_recipes(self):
        recipes_data = [
            {
                'name': 'Амулет Слаймов',
                'image': 'craft-items/slime_amulet.png',
                'effect': 'Увеличивает удачу в 2.5 раза',
                'effect_type': 'LuckBoost',
                'effect_value': 2.5,
                'ingredients': [
                    ('Зелёный Слайм', 5),
                    ('Синий Слайм', 2),
                    ('Электрический Слайм', 1),
                ]
            },
            {
                'name': 'Амулет Урожая',
                'image': 'craft-items/harves_amulet.png',
                'effect': 'Увеличивает получаемое количество слаймов на 1',
                'effect_type': 'HarvestMultiplier',
                'effect_value': 1,
                'ingredients': [
                    ('Зелёный Слайм', 20),
                    ('Жёлтый Слайм', 5),
                    ('Золотой Слайм', 1),
                ]
            },
            {
                'name': 'Амулет Вечности',
                'image': 'craft-items/infinity_amulet.png',
                'effect': 'Увеличивает удачу в 10 раз',
                'effect_type': 'LuckBoost',
                'effect_value': 10,
                'ingredients': [
                    ('Лунный Слайм', 1),
                    ('Солнечный Слайм', 1),
                    ('Временной Слайм', 1),
                ]
            },
            {
                'name': 'Амулет Изобилия',
                'image': 'craft-items/abundance_amulet.png',
                'effect': 'Получаешь на одного слайма больше',
                'effect_type': 'HarvestMultiplier',
                'effect_value': 1,
                'ingredients': [
                    ('Фиолетовый Слайм', 10),
                    ('Оранжевый Слайм', 5),
                    ('Божественный Слайм', 1),
                ]
            },
            {
                'name': 'Амулет удачи',
                'image': 'craft-items/Lucky_amulet.png',
                'effect': 'Увеличивает шанс найти редкого слайма в 2 раза',
                'effect_type': 'LuckBoost',
                'effect_value': 2,
                'ingredients': [
                    ('Зелёный Слайм', 10),
                    ('Синий Слайм', 5),
                ]
            },
            {
                'name': 'Амулет скорости',
                'image': 'craft-items/speed_amulet.png',
                'effect': 'Уменьшает время восстановления спина на 20%',
                'effect_type': 'SpinCooldown',
                'effect_value': 0.8,
                'ingredients': [
                    ('Красный Слайм', 10),
                    ('Жёлтый Слайм', 5),
                ]
            },
        ]

        for recipe_data in recipes_data:
            recipe, created = CraftRecipe.objects.get_or_create(
                name=recipe_data['name'],
                defaults={
                    'image': recipe_data['image'],
                    'effect': recipe_data['effect'],
                    'effect_type': recipe_data['effect_type'],
                    'effect_value': recipe_data['effect_value'],
                    'created_by_default': True,
                }
            )
            
            if created:
                self.stdout.write(f"Created recipe: {recipe.name}")
                
                # Add ingredients
                for slime_name, amount in recipe_data['ingredients']:
                    try:
                        slime_type = SlimeType.objects.get(name=slime_name)
                        CraftIngredient.objects.create(
                            recipe=recipe,
                            slime_type=slime_type,
                            amount=amount
                        )
                    except SlimeType.DoesNotExist:
                        self.stdout.write(f"Warning: SlimeType '{slime_name}' not found for recipe {recipe.name}")

    def create_collections(self):
        collections_data = [
            {
                'name': 'Начальные слаймы',
                'description': 'Собери всех основных слаймов',
                'reward': 'Увеличивает удачу в 2 раза',
                'effect_type': 'LuckBoost',
                'effect_value': 2,
                'requirements': [
                    ('Зелёный Слайм', 1),
                    ('Синий Слайм', 1),
                    ('Красный Слайм', 1),
                    ('Жёлтый Слайм', 1),
                ]
            },
            {
                'name': 'Элементальные слаймы',
                'description': 'Собери слаймов всех стихий',
                'reward': 'Увеличивает получаемое количество слаймов на 1',
                'effect_type': 'HarvestMultiplier',
                'effect_value': 1,
                'requirements': [
                    ('Ледяной Слайм', 1),
                    ('Огненный Слайм', 1),
                    ('Электрический Слайм', 1),
                    ('Водный Слайм', 1),
                ]
            },
            {
                'name': 'Редкие экземпляры',
                'description': 'Собери самых редких слаймов',
                'reward': 'Уменьшает время восстановления спина на 30%',
                'effect_type': 'SpinCooldown',
                'effect_value': 0.7,
                'requirements': [
                    ('Космический Слайм', 1),
                    ('Временной Слайм', 1),
                    ('Божественный Слайм', 1),
                ]
            },
            {
                'name': 'Все обычные',
                'description': 'Собери по 10 экземпляров каждого обычного слайма',
                'thumbnail': 'collections/common_slimes.png',
                'reward': 'Дает х5 удачи',
                'effect_type': 'LuckBoost',
                'effect_value': 5,
                'requirements': [
                    ('Зелёный Слайм', 10),
                    ('Синий Слайм', 10),
                    ('Красный Слайм', 10),
                    ('Жёлтый Слайм', 10),
                    ('Фиолетовый Слайм', 10),
                    ('Оранжевый Слайм', 10),
                ]
            },
            {
                'name': 'Мифический набор',
                'description': 'Собери всех мифических слаймов',
                'reward': 'Удваивает удачу в 5 раз',
                'effect_type': 'LuckBoost',
                'effect_value': 5,
                'requirements': [
                    ('Временной Слайм', 1),
                    ('Портальный Слайм', 1),
                    ('Слайм Земля', 1),
                    ('Читер Слайм', 1),
                ]
            },
        ]

        for collection_data in collections_data:
            collection, created = Collection.objects.get_or_create(
                name=collection_data['name'],
                defaults={
                    'description': collection_data['description'],
                    'reward': collection_data['reward'],
                    'effect_type': collection_data['effect_type'],
                    'effect_value': collection_data['effect_value'],
                    'thumbnail': collection_data.get('thumbnail'),
                }
            )
            
            if created:
                self.stdout.write(f"Created collection: {collection.name}")
                
                # Add requirements
                for slime_name, amount in collection_data['requirements']:
                    try:
                        slime_type = SlimeType.objects.get(name=slime_name)
                        CollectionRequirement.objects.create(
                            collection=collection,
                            slime_type=slime_type,
                            amount=amount
                        )
                    except SlimeType.DoesNotExist:
                        self.stdout.write(f"Warning: SlimeType '{slime_name}' not found for collection {collection.name}")

        self.stdout.write(self.style.SUCCESS('Successfully populated all data!'))