from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    # Настройки игрока
    animation_enabled = models.BooleanField(default=True)
    auto_save_enabled = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)
    collections_visible = models.BooleanField(default=True)
    index_visible = models.BooleanField(default=True)
    
    # Статистика
    total_spins = models.PositiveIntegerField(default=0)
    rare_slimes_found = models.PositiveIntegerField(default=0)
    
    # Бонусы
    harvest_multiplier = models.FloatField(default=1.0)
    spin_cooldown = models.PositiveIntegerField(default=1000)  # в ms
    luck = models.FloatField(default=0.0)
    
    
    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"

class SlimeType(models.Model):
    RARITY_CHOICES = [
        ('common', 'Обычный'),
        ('uncommon', 'Необычный'),
        ('rare', 'Редкий'),
        ('epic', 'Эпический'),
        ('legendary', 'Легендарный'),
        ('mythic', 'Мифический'),
        ('divine', 'Божественный'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='slimes/', null=True, blank=True)  # Путь к файлу в media/slimes/
    chance = models.CharField(max_length=50)  # Формат "1/1000"
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES)
    base_amount = models.PositiveIntegerField(default=0)  # Для начальных значений
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип слайма"
        verbose_name_plural = "Типы слаймов"
        ordering = ['chance']

class CraftRecipe(models.Model):
    HARVESTMULTIPLIER = 'HarvestMultiplier'
    SPINCOOLDOWN = 'SpinCooldown'
    LUCKBOOST = 'LuckBoost'

    EFFECT_TYPE_CHOICES = [
        (HARVESTMULTIPLIER, 'HarvestMultiplier'),
        (SPINCOOLDOWN, 'SpinCooldown'),
        (LUCKBOOST, 'LuckBoost'),
    ]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='craft-items/', null=True, blank=True)
    effect = models.TextField()
    created_by_default = models.BooleanField(default=False)
    effect_type = models.CharField(max_length=50, choices=EFFECT_TYPE_CHOICES, default=LUCKBOOST, null=True, blank=True)
    effect_value = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Рецепт крафта"
        verbose_name_plural = "Рецепты крафта"

class CraftIngredient(models.Model):
    recipe = models.ForeignKey(CraftRecipe, on_delete=models.CASCADE, related_name='ingredients')
    slime_type = models.ForeignKey(SlimeType, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.recipe.name} - {self.slime_type.name} - {self.amount}"
    
    class Meta:
        unique_together = ('recipe', 'slime_type')
        verbose_name = "Ингредиент крафта"
        verbose_name_plural = "Ингредиенты крафта"

class Collection(models.Model):
    HARVESTMULTIPLIER = 'HarvestMultiplier'
    SPINCOOLDOWN = 'SpinCooldown'
    LUCKBOOST = 'LuckBoost'

    EFFECT_TYPE_CHOICES = [
        (HARVESTMULTIPLIER, 'HarvestMultiplier'),
        (SPINCOOLDOWN, 'SpinCooldown'),
        (LUCKBOOST, 'LuckBoost'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='collections/', null=True, blank=True)
    reward = models.TextField()
    effect_type = models.CharField(max_length=50, choices=EFFECT_TYPE_CHOICES, default=LUCKBOOST, null=True, blank=True)
    effect_value = models.FloatField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    claimed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"

class CollectionRequirement(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='requirements')
    slime_type = models.ForeignKey(SlimeType, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('collection', 'slime_type')
        verbose_name = "Требование коллекции"
        verbose_name_plural = "Требования коллекций"

class PlayerInventory(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory')
    slime_type = models.ForeignKey(SlimeType, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('player', 'slime_type')
        verbose_name = "Инвентарь игрока"
        verbose_name_plural = "Инвентари игроков"
        indexes = [
            models.Index(fields=['player', 'slime_type']),
        ]

class PlayerCraft(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crafts')
    recipe = models.ForeignKey(CraftRecipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('player', 'recipe')
        verbose_name = "Созданный предмет"
        verbose_name_plural = "Созданные предметы"

class PlayerCollection(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    claimed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('player', 'collection')
        verbose_name = "Коллекция игрока"
        verbose_name_plural = "Коллекции игроков"
