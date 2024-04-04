from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from .models import MenuItem, Ingredient, Recipe, Order
from django.views.generic.edit import CreateView, UpdateView
from .forms import IngredientCreateForm, MenuItemCreateForm, RecipeCreateForm, OrderCreateForm
from django.shortcuts import get_object_or_404
import decimal
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin


def login_view(request):
    """
    This function authenticates the user and logs them in
    :param request:
    :return:
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('menu_list')

    return redirect('signup')


def logout_view(request):
    """
    This function logs out the user
    :param request:
    :return:
    """
    logout(request)
    return redirect('login')


class MenuListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = 'menu_app/menu_list.html'
    context_object_name = 'menu_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add dictionary representation of each MenuItem to the context
        context['menu_items_dict'] = [item.as_dict() for item in context['menu_items']]
        return context


class MenuItemCreateView(LoginRequiredMixin, CreateView):
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


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = 'menu_app/ingredient_create_form.html'


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = 'menu_app/ingredient_update_form.html'


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeCreateForm
    template_name = 'menu_app/recipe_create_form.html'

    def post(self, request, *args, **kwargs):
        menu_item = get_object_or_404(MenuItem, pk=request.POST['menu_item'])
        ingredient = get_object_or_404(Ingredient, pk=request.POST['ingredient'])
        quantity = decimal.Decimal(request.POST['quantity'])
        recipe = Recipe(menu_item=menu_item, ingredient=ingredient, quantity=quantity)
        if not recipe.enough():
            return render(request, 'menu_app/recipe_create_form.html', {'form': super().get_form(),
                                                                        'error': 'Not enough ingredients'})
        return super().post(request, *args, **kwargs)


class RecipeListView(LoginRequiredMixin, ListView):
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


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'menu_app/order_create_form.html'
    form_class = OrderCreateForm

    def post(self, request, *args, **kwargs):
        menu_item = super().get_form_kwargs()['data']['menu_item']
        ingredients = Recipe.objects.filter(menu_item=menu_item).values('ingredient', 'quantity')
        for ingredient in ingredients:
            store_ingredient = Ingredient.objects.get(pk=ingredient['ingredient'])
            store_ingredient.quantity -= decimal.Decimal(ingredient['quantity'])
            store_ingredient.save()
        return super().post(request, *args, **kwargs)


class OrderListView(LoginRequiredMixin, ListView):
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


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"
