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
from django.utils.dateparse import parse_datetime
from django.utils import timezone

@method_decorator(csrf_exempt, name='dispatch')
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
            all_crafts = CraftRecipe.objects.all()  # Изменено название переменной
            for craft in all_crafts:
                PlayerCraft.objects.create(player=user, recipe=craft)

            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
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

@method_decorator(csrf_exempt, name='dispatch')
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





@method_decorator(csrf_exempt, name='dispatch')
class SaveGameView(APIView):
    permission_classes = [permissions.IsAuthenticated]
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
        
        # Сохранение крафтов (с обработкой created и ошибок)
        PlayerCraft.objects.filter(player=request.user).delete()
        crafts_to_create = []
        for craft_data in request.data.get('crafts', []):
            try:
                recipe = CraftRecipe.objects.get(id=craft_data['recipe']['id'])
                
                # Обновляем или создаем запись PlayerCraft
                player_craft, created = PlayerCraft.objects.update_or_create(
                    player=request.user,
                    recipe=recipe,
                    defaults={
                        'is_completed': craft_data.get('is_completed', False)
                    }
                )
            except (KeyError, CraftRecipe.DoesNotExist):
                continue
        
        PlayerCraft.objects.bulk_create(crafts_to_create)
        
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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        with transaction.atomic():
            all_slime_types = SlimeType.objects.all()
            for slime_type in all_slime_types:
                PlayerInventory.objects.get_or_create(player=request.user, slime_type=slime_type)
            
            all_crafts = CraftRecipe.objects.all()  # Исправлено: убрана фильтрация по пользователю
            for craft in all_crafts:
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
