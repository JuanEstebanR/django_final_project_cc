from django.shortcuts import render
from django.views.generic import ListView
from .models import MenuItem, Ingredient, Recipe, Order


# Create your views here.
class menu_list(ListView):
    model = MenuItem
    template_name = "menu_app/base.html"
    context_object_name = "menu_items"
