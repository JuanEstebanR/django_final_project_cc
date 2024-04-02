from django.contrib import admin
from .models import Ingredient, Recipe, MenuItem, Order
# Register your models here.
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(MenuItem)
admin.site.register(Order)
