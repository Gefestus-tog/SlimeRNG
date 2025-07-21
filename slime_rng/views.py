from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @transaction.atomic
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Создание инвентаря для всех типов слаймов
            all_slime_types = SlimeType.objects.all()
            for slime_type in all_slime_types:
                PlayerInventory.objects.create(player=user, slime_type=slime_type, amount=slime_type.base_amount)
            
            # Создание записей для всех коллекций
            all_collections = Collection.objects.all()
            for collection in all_collections:
                PlayerCollection.objects.create(player=user, collection=collection)
            
            # Создание предметов по умолчанию
            default_crafts = CraftRecipe.objects.all()
            for craft in default_crafts:
                PlayerCraft.objects.create(player=user, recipe=craft)

            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id
                })
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

class SlimeTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SlimeType.objects.all()
    serializer_class = SlimeTypeSerializer

class CraftRecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CraftRecipe.objects.prefetch_related('ingredients__slime_type').all()
    serializer_class = CraftRecipeSerializer

class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Collection.objects.prefetch_related('requirements__slime_type').all()
    serializer_class = CollectionSerializer

class PlayerInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerInventorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PlayerInventory.objects.filter(player=self.request.user)

class PlayerInventoryView(APIView):
    def get(self, request):
        inventory = PlayerInventory.objects.filter(player=request.user)
        serializer = PlayerInventorySerializer(inventory, many=True)
        return Response(serializer.data)

class CraftItemView(APIView):
    @transaction.atomic
    def post(self, request, recipe_id):
        try:
            recipe = CraftRecipe.objects.get(id=recipe_id)
            ingredients = recipe.ingredients.all()
            
            # Проверка ингредиентов
            for ingredient in ingredients:
                try:
                    item = PlayerInventory.objects.get(
                        player=request.user,
                        slime_type=ingredient.slime_type
                    )
                    if item.amount < ingredient.amount:
                        return Response(
                            {'error': f'Not enough {ingredient.slime_type.name}'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except PlayerInventory.DoesNotExist:
                    return Response(
                        {'error': f'Missing {ingredient.slime_type.name}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Списание ингредиентов
            for ingredient in ingredients:
                item = PlayerInventory.objects.get(
                    player=request.user,
                    slime_type=ingredient.slime_type
                )
                item.amount -= ingredient.amount
                item.save()
            
            # Создание предмета
            PlayerCraft.objects.create(player=request.user, recipe=recipe)
            
            # Применение эффекта
            if recipe.effect_type and recipe.effect_value:
                apply_recipe_effect(request.user, recipe)
            
            return Response(status=status.HTTP_201_CREATED)
        
        except CraftRecipe.DoesNotExist:
            return Response({'error': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)

def apply_recipe_effect(user, recipe):
    if recipe.effect_type == 'harvestMultiplier':
        user.harvest_multiplier += recipe.effect_value
    elif recipe.effect_type == 'spinCooldown':
        user.spin_cooldown = max(100, user.spin_cooldown * (1 - recipe.effect_value))
    elif recipe.effect_type == 'rareChanceBoost':
        user.rare_chance_boost += recipe.effect_value
    elif recipe.effect_type == 'epicChanceBoost':
        user.epic_chance_boost += recipe.effect_value
    elif recipe.effect_type == 'divineChanceMultiplier':
        user.divine_chance_multiplier *= recipe.effect_value
    user.save()

class ClaimCollectionView(APIView):
    @transaction.atomic
    def post(self, request, collection_id):
        try:
            collection = Collection.objects.get(id=collection_id)
            player_collection, _ = PlayerCollection.objects.get_or_create(
                player=request.user,
                collection=collection
            )
            
            if player_collection.claimed:
                return Response(
                    {'error': 'Reward already claimed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Проверка требований
            requirements = collection.requirements.all()
            for req in requirements:
                try:
                    item = PlayerInventory.objects.get(
                        player=request.user,
                        slime_type=req.slime_type
                    )
                    if item.amount < req.amount:
                        return Response(
                            {'error': f'Not enough {req.slime_type.name}'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except PlayerInventory.DoesNotExist:
                    return Response(
                        {'error': f'Missing {req.slime_type.name}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Обновление статуса
            player_collection.completed = True
            player_collection.claimed = True
            player_collection.save()
            
            # Применение эффекта
            if collection.effect_type and collection.effect_value:
                apply_collection_effect(request.user, collection)
            
            return Response(status=status.HTTP_200_OK)
        
        except Collection.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

def apply_collection_effect(user, collection):
    if collection.effect_type == 'harvestMultiplier':
        user.harvest_multiplier += collection.effect_value
    elif collection.effect_type == 'spinCooldown':
        user.spin_cooldown = max(100, user.spin_cooldown * (1 - collection.effect_value))
    elif collection.effect_type == 'rareChanceBoost':
        user.rare_chance_boost += collection.effect_value
    elif collection.effect_type == 'epicChanceBoost':
        user.epic_chance_boost += collection.effect_value
    elif collection.effect_type == 'divineChanceMultiplier':
        user.divine_chance_multiplier *= collection.effect_value
    user.save()

class SaveGameView(APIView):
    @transaction.atomic
    def post(self, request):
        # Сохранение состояния пользователя
        user_serializer = UserSerializer(request.user, data=request.data.get('user'), partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        
        # Сохранение инвентаря
        for item_data in request.data.get('inventory', []):
            slime_type = SlimeType.objects.get(id=item_data['slime_type']['id'])
            PlayerInventory.objects.update_or_create(
                player=request.user,
                slime_type=slime_type,
                defaults={'amount': item_data['amount']}
            )
        
        # Сохранение крафтов
        PlayerCraft.objects.filter(player=request.user).delete()
        for craft_data in request.data.get('crafts', []):
            recipe = CraftRecipe.objects.get(id=craft_data['recipe']['id'])
            PlayerCraft.objects.create(player=request.user, recipe=recipe)
        
        # Сохранение коллекций
        for col_data in request.data.get('collections', []):
            collection = Collection.objects.get(id=col_data['collection']['id'])
            PlayerCollection.objects.update_or_create(
                player=request.user,
                collection=collection,
                defaults={
                    'completed': col_data['completed'],
                    'claimed': col_data['claimed']
                }
            )
        
        return Response(status=status.HTTP_200_OK)

class LoadGameView(APIView):
    def get(self, request):
        with transaction.atomic():
            all_slime_types = SlimeType.objects.all()
            for slime_type in all_slime_types:
                PlayerInventory.objects.get_or_create(player=request.user, slime_type=slime_type)
            
            default_crafts = CraftRecipe.objects.filter(created_by_default=True)
            for craft in default_crafts:
                PlayerCraft.objects.get_or_create(player=request.user, recipe=craft)

        inventory_qs = PlayerInventory.objects.filter(player=request.user).order_by('slime_type__id')

        data = {
            'user': UserSerializer(request.user).data,
            'inventory': PlayerInventorySerializer(inventory_qs, many=True).data,
            'crafts': PlayerCraftSerializer(
                PlayerCraft.objects.filter(player=request.user),
                many=True
            ).data,
            'collections': PlayerCollectionSerializer(
                PlayerCollection.objects.filter(player=request.user),
                many=True
            ).data,
        }
        return Response(data)
