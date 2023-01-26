# from django.db.models import Sum
# from django.contrib.auth import get_user_model
# from django.shortcuts import get_list_or_404, get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
# from djoser.views import UserViewSet
# from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag, IngredientAmount
# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

# from .filters import IngredientFilter, RecipeFilter
# from .pagination import CustomPagination
# from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
# from .utils import create_pdf
# from api.serializers import (
#     CustomUserSerializer, FavoriteSerializer, FollowSerializer,
#     IngredientSerializer, RecipeReadSerializer, RecipeWriteSerializer,
#     ShoppingCartSerializer, ShortRecipeSerializer, TagSerializer, SimpleRecipeSerializer
# )
# from users.models import Follow, User

# User = get_user_model()


# class CustomUserViewSet(UserViewSet):
#     queryset = User.objects.all()
#     serializer_class = CustomUserSerializer
#     pagination_class = CustomPagination

#     @action(
#         detail=True,
#         methods=['GET', 'POST', 'DELETE'],
#         url_path='subscribe',
#         permission_classes=[IsAuthenticated]
#     )
#     def subscribe(self, request, id, **kwargs):
#         # user = request.user
#         # author_id = self.kwargs.get('id')
#         # author = get_object_or_404(User, id=author_id)

#         # if request.method == 'POST':
#         #     serializer = FollowSerializer(author,
#         #                                   data=request.data,
#         #                                   context={"request": request})
#         #     serializer.is_valid(raise_exception=True)
#         #     Follow.objects.create(user=user, author=author)
#         #     return Response(serializer.data, status=status.HTTP_201_CREATED)

#         # if request.method == 'DELETE':
#         #     subscription = get_object_or_404(Follow,
#         #                                      user=user,
#         #                                      author=author)
#         #     subscription.delete()
#         #     return Response(status=status.HTTP_204_NO_CONTENT)
#         # serializer = FollowSerializer()
#         # return Response(serializer.data, status=status.HTTP_200_OK)
#         author_id = id
#         if request.method == 'POST':
#             author = get_object_or_404(User, id=author_id)
#             serializer = FollowSerializer(author, context={'request': request})
#             serializer.validate(serializer.data)
#             Follow.objects.create(
#                 user=request.user, author=author
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         user_id = request.user.id
#         subscribe = get_object_or_404(
#             Follow, user__id=user_id, author__id=author_id
#         )
#         subscribe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     @action(
#         detail=False,
#         url_path='subscriptions',
#         permission_classes=[IsAuthenticated]
#     )
#     def subscriptions(self, request):
#         user = request.user
#         queryset = User.objects.filter(following__user=user)
#         pages = self.paginate_queryset(queryset)
#         serializer = FollowSerializer(pages,
#                                       many=True,
#                                       context={'request': request})
#         return self.get_paginated_response(serializer.data)


# class IngredientViewSet(ReadOnlyModelViewSet):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#     permission_classes = (IsAdminOrReadOnly,)
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = IngredientFilter


# class TagViewSet(ReadOnlyModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = (IsAdminOrReadOnly,)


# class RecipeViewSet(ModelViewSet):
#     queryset = Recipe.objects.all()
#     permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
#     pagination_class = CustomPagination
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = RecipeFilter

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     def get_serializer_class(self):
#         if self.request.method in SAFE_METHODS:
#             return RecipeReadSerializer
#         return RecipeWriteSerializer
     
#     @staticmethod
#     def _add_recipe_to(request, pk, model, my_serializer):
#         recipe_id = pk
#         if request.method == 'POST':
#             recipe = get_object_or_404(Recipe, id=recipe_id)
#             serializer = my_serializer(
#                 recipe, context={'request': request}
#             )
#             serializer.validate(serializer.data)
#             model.objects.create(user=request.user, recipe=recipe)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         user_id = request.user.id
#         recipe = get_object_or_404(
#             model, user__id=user_id,
#             recipe__id=recipe_id
#         )
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     @action(
#         detail=True,
#         methods=['POST', 'DELETE'],
#         permission_classes=[IsAuthenticated]
#     )
#     def favorite(self, request, pk):
#         return self._add_recipe_to(request, pk, Favorite, FavoriteSerializer)

#     @action(
#         detail=True,
#         methods=['POST', 'DELETE'],
#         permission_classes=[IsAuthenticated]
#     )
#     def shopping_cart(self, request, pk):
#         return self._add_recipe_to(
#             request, pk, ShoppingCart, SimpleRecipeSerializer
#         )
#     #     if request.method == 'POST':
#     #         return self.add_to(ShoppingCart, request.user, pk)
#     #     serializer = ShoppingCartSerializer()
#     #     return Response(serializer.data, status=status.HTTP_200_OK)

#     # def add_to(self, model, user, pk):
#     #     if model.objects.filter(user=user, recipe__id=pk).exists():
#     #         return Response({'errors': 'Рецепт уже добавлен!'},
#     #                         status=status.HTTP_400_BAD_REQUEST)
#     #     recipe = get_object_or_404(Recipe, id=pk)
#     #     model.objects.create(user=user, recipe=recipe)
#     #     serializer = ShortRecipeSerializer(recipe)
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)

#     # def delete_from(self, model, user, pk):
#     #     obj = model.objects.filter(user=user, recipe__id=pk)
#     #     if obj.exists():
#     #         obj.delete()
#     #         return Response(status=status.HTTP_204_NO_CONTENT)
#     #     return Response({'errors': 'Рецепт уже удален!'},
#     #                     status=status.HTTP_400_BAD_REQUEST)

#     @action(
#         detail=False,
#         methods=['GET'],
#         url_path='download_shopping_cart',
#         permission_classes=[IsAuthenticated]
#     )
#     def download_shopping_cart(self, request):
#         user = request.user
#         ingredients = IngredientAmount.objects.filter(
#             recipe__shopping_cart__user=user
#         ).values(
#             'ingredient__name', 'ingredient__measurement_unit'
#         ).order_by(
#         'ingredient__name'
#         ).annotate(
#             sum_amount=Sum('amount')
#         )
#         return create_pdf(ingredients)
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag, IngredientAmount
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .utils import create_pdf
from api.serializers import (
    CustomUserSerializer, FavoriteSerializer, FollowSerializer,
    IngredientSerializer, RecipeReadSerializer, RecipeWriteSerializer, TagSerializer, SimpleRecipeSerializer,
    # ShoppingCartSerializer, ShortRecipeSerializer,
)
from users.models import Follow, User

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(
        detail=True,
        methods=['GET', 'POST', 'DELETE'],
        url_path='subscribe',
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id, **kwargs):
        # user = request.user
        # author_id = self.kwargs.get('id')
        # author = get_object_or_404(User, id=author_id)

        # if request.method == 'POST':
        #     serializer = FollowSerializer(author,
        #                                   data=request.data,
        #                                   context={"request": request})
        #     serializer.is_valid(raise_exception=True)
        #     Follow.objects.create(user=user, author=author)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)

        # if request.method == 'DELETE':
        #     subscription = get_object_or_404(Follow,
        #                                      user=user,
        #                                      author=author)
        #     subscription.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        # serializer = FollowSerializer()
        # return Response(serializer.data, status=status.HTTP_200_OK)
        author_id = id
        if request.method == 'POST':
            author = get_object_or_404(User, id=author_id)
            serializer = FollowSerializer(author, context={'request': request})
            serializer.validate(serializer.data)
            Follow.objects.create(
                user=request.user, author=author
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        user_id = request.user.id
        subscribe = get_object_or_404(
            Follow, user__id=user_id, author__id=author_id
        )
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        url_path='subscriptions',
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(pages,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer
     
    @staticmethod
    def _add_recipe_to(request, pk, model, my_serializer):
        recipe_id = pk
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=recipe_id)
            serializer = my_serializer(
                recipe, context={'request': request}
            )
            serializer.validate(serializer.data)
            model.objects.create(user=request.user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        user_id = request.user.id
        recipe = get_object_or_404(
            model, user__id=user_id,
            recipe__id=recipe_id
        )
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        return self._add_recipe_to(request, pk, Favorite, FavoriteSerializer)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return self._add_recipe_to(
            request, pk, ShoppingCart, SimpleRecipeSerializer
        )
    #     if request.method == 'POST':
    #         return self.add_to(ShoppingCart, request.user, pk)
    #     serializer = ShoppingCartSerializer()
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def add_to(self, model, user, pk):
    #     if model.objects.filter(user=user, recipe__id=pk).exists():
    #         return Response({'errors': 'Рецепт уже добавлен!'},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #     recipe = get_object_or_404(Recipe, id=pk)
    #     model.objects.create(user=user, recipe=recipe)
    #     serializer = ShortRecipeSerializer(recipe)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def delete_from(self, model, user, pk):
    #     obj = model.objects.filter(user=user, recipe__id=pk)
    #     if obj.exists():
    #         obj.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     return Response({'errors': 'Рецепт уже удален!'},
    #                     status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
        'ingredient__name'
        ).annotate(
            sum_amount=Sum('amount')
        )
        return create_pdf(ingredients)
