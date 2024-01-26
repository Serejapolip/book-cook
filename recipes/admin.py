from django.contrib import admin
from .models import Recipe,Product, RecipeProduct

class RecipeProductInline(admin.StackedInline):
    model = RecipeProduct

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeProductInline]

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Product)
