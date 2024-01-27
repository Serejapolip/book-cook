from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.db import transaction





from .models import Product, Recipe, RecipeProduct

def add_product_to_recipe(request):
    recipe_id = request.GET.get('recipe_id')
    product_id = request.GET.get('product_id')
    weight = request.GET.get('weight')

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    product = get_object_or_404(Product, pk=product_id)
    recipe_product, _ = RecipeProduct.objects.update_or_create(recipe=recipe, product=product)
    recipe_product.weight = weight
    recipe_product.save()

    return HttpResponse('Success')

def cook_recipe(request):
    recipe_id = request.GET.get('recipe_id')

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe_products = recipe.recipeproduct_set.all()

    with transaction.atomic():
        for recipe_product in recipe_products:
            recipe_product.product.times_cooked += 1
            recipe_product.product.save()

    return HttpResponse('Success')

def show_recipes_without_product(request):
    product_id = request.GET.get('product_id')

    recipes = Recipe.objects.filter(~Q(recipeproduct__product_id=product_id) | Q(recipeproduct__weight__lt=10, recipeproduct__product_id=product_id)).distinct()
    print(str(recipes.query))

    
    

    return render(request, './recipes_without_product.html', {'recipes': recipes, 'product': Product.objects.get(pk=product_id)})