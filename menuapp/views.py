from django.shortcuts import render
from django.views.generic import ListView
from .models import MenuItem, Ingredient, Recipe, Order
from django.views.generic.edit import CreateView, UpdateView
from .forms import IngredientCreateForm, MenuItemCreateForm, RecipeCreateForm, OrderCreateForm
from django.shortcuts import get_object_or_404
import decimal
from django.db.models import Sum


# Create your views here.
class MenuListView(ListView):
    model = MenuItem
    template_name = 'menu_app/menu_list.html'
    context_object_name = 'menu_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add dictionary representation of each MenuItem to the context
        context['menu_items_dict'] = [item.as_dict() for item in context['menu_items']]
        return context


class MenuItemCreateView(CreateView):
    model = MenuItem
    template_name = 'menu_app/menu_create_form.html'
    form_class = MenuItemCreateForm


class IngredientListView(ListView):
    model = Ingredient
    context_object_name = 'ingredients'
    template_name = 'menu_app/ingredients_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add dictionary representation of each MenuItem to the context
        context['ingredients_dict'] = [item.as_dict() for item in context['ingredients']]
        return context


class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = 'menu_app/ingredient_create_form.html'
    success_url = '/menu/ingredients'


class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = 'menu_app/ingredient_update_form.html'
    success_url = '/menu/ingredients'


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeCreateForm
    template_name = 'menu_app/recipe_create_form.html'
    success_url = '/menu/recipes'

    def post(self, request, *args, **kwargs):
        menu_item = get_object_or_404(MenuItem, pk=request.POST['menu_item'])
        ingredient = get_object_or_404(Ingredient, pk=request.POST['ingredient'])
        quantity = decimal.Decimal(request.POST['quantity'])
        recipe = Recipe(menu_item=menu_item, ingredient=ingredient, quantity=quantity)
        if not recipe.enough():
            return render(request, 'menu_app/recipe_create_form.html', {'form': super().get_form(),
                                                                        'error': 'Not enough ingredients'})
        return super().post(request, *args, **kwargs)


class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'menu_app/recipe_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes_dict'] = [item.as_dict() for item in context['recipes']]
        recipes_names = {}
        for recipe_dict in context['recipes_dict']:
            menu_item = recipe_dict['menu_item']
            if menu_item.name not in recipes_names:
                recipes_names[menu_item.name] = {}
            ingredient_name = recipe_dict['ingredient']
            recipes_names[menu_item.name][ingredient_name.name] = recipe_dict['quantity']
        context['recipes'] = recipes_names
        return context


class OrderCreateView(CreateView):
    model = Order
    template_name = 'menu_app/order_create_form.html'
    form_class = OrderCreateForm
    success_url = '/menu/orders'

    def post(self, request, *args, **kwargs):
        menu_item = super().get_form_kwargs()['data']['menu_item']
        ingredients = Recipe.objects.filter(menu_item=menu_item).values('ingredient', 'quantity')
        for ingredient in ingredients:
            store_ingredient = Ingredient.objects.get(pk=ingredient['ingredient'])
            store_ingredient.quantity -= decimal.Decimal(ingredient['quantity'])
            store_ingredient.save()
        return super().post(request, *args, **kwargs)


class OrderListView(ListView):
    model = Order
    template_name = 'menu_app/order_list.html'
    context_object_name = 'orders'
    ordering = ['order_date']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        orders = Order.objects.all()
        revenue = Order.objects.aggregate(revenue=Sum("menu_item__price"))['revenue']
        total_cost = 0
        for order in orders:
            for recipe_ingredient in order.menu_item.recipe_set.all():
                total_cost += recipe_ingredient.ingredient.price_per_unit * recipe_ingredient.quantity

        context['revenue'] = revenue
        context['orders'] = orders
        context['profit'] = revenue - total_cost
        context['total_cost'] = total_cost
        return context
