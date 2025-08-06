from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    User, SlimeType, CraftRecipe, CraftIngredient, 
    Collection, CollectionRequirement, PlayerInventory,
    PlayerCraft, PlayerCollection
)
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'password',
            'animation_enabled', 'auto_save_enabled',
            'collections_visible', 'index_visible', 'total_spins', 'rare_slimes_found',
            'harvest_multiplier', 'spin_cooldown', 'rare_chance_boost',
            'epic_chance_boost', 'divine_chance_multiplier'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class SlimeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlimeType
        fields = ['id', 'name', 'image', 'chance', 'rarity', 'base_amount']

class CraftIngredientSerializer(serializers.ModelSerializer):
    slime_type = SlimeTypeSerializer()
    
    class Meta:
        model = CraftIngredient
        fields = ['slime_type', 'amount']

class CraftRecipeSerializer(serializers.ModelSerializer):
    ingredients = CraftIngredientSerializer(many=True)
    
    class Meta:
        model = CraftRecipe
        fields = ['id', 'name', 'image', 'effect', 'effect_type', 'effect_value', 'ingredients']

class CollectionRequirementSerializer(serializers.ModelSerializer):
    slime_type = SlimeTypeSerializer()
    
    class Meta:
        model = CollectionRequirement
        fields = ['slime_type', 'amount']

class CollectionSerializer(serializers.ModelSerializer):
    requirements = CollectionRequirementSerializer(many=True)
    
    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'thumbnail', 'reward', 'effect_type', 'effect_value', 'requirements']

class PlayerInventorySerializer(serializers.ModelSerializer):
    slime_type = SlimeTypeSerializer()
    
    class Meta:
        model = PlayerInventory
        fields = ['slime_type', 'amount', 'last_updated']

class PlayerCraftSerializer(serializers.ModelSerializer):
    recipe = CraftRecipeSerializer()
    
    class Meta:
        model = PlayerCraft
        fields = ['recipe', 'created_at', 'is_completed']
        read_only_fields = ['created_at']  # Добавлено для безопасности

class PlayerCollectionSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer()
    
    class Meta:
        model = PlayerCollection
        fields = ['collection', 'completed', 'claimed', 'completed_at']

class GameStateSerializer(serializers.Serializer):
    user = UserSerializer()
    inventory = PlayerInventorySerializer(many=True)
    crafts = PlayerCraftSerializer(many=True)
    collections = PlayerCollectionSerializer(many=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()