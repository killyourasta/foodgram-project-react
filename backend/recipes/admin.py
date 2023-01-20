from django.contrib import admin
from django.contrib.admin import display
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    Favorite, Ingredient, IngredientAmount, Recipe, ShoppingCart, Tag,
)

EMPTY_VALUE_DISPLAY = '-пусто-'


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientResource]


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1
    min_num = 1
    list_display = ('name', 'measurement_unit')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color')
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author',)
    list_filter = ('name', 'author', 'tags',)
    inlines = [RecipeIngredientInline, ]
    readonly_fields = ('added_in_favorites',)
    empty_value_display = EMPTY_VALUE_DISPLAY

    @display(description='Общее число добавлений в избранное')
    def added_in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = EMPTY_VALUE_DISPLAY


admin.site.register(Ingredient, IngredientAdmin)
