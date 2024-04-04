from django.db import models
from django.urls import reverse


# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'menuapp_menuitem'

    def __str__(self):
        return "Menu: {0} - Price: {1}".format(self.name, self.price)

    def as_dict(self):
        """
        Returns the object as a dictionary
        :return:
        """
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price
        }

    def get_absolute_url(self):
        """
        Returns the absolute url for the object
        :return:
        """
        return reverse('menu_list')


class Ingredient(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    unit = models.CharField(max_length=50)
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'menuapp_ingredient'

    def __str__(self):
        return "{0} - Price per unit: {1}, Quantity: {2}".format(self.name, self.price_per_unit, self.quantity)

    def as_dict(self):
        """
        Returns the object as a dictionary
        :return:
        """
        return {
            "name": self.name,
            "unit": self.unit,
            "price_per_unit": self.price_per_unit,
            "quantity": self.quantity,
        }

    def get_absolute_url(self):
        """
        Returns the absolute url for the object
        :return:
        """
        return reverse('ingredient_list')


class Recipe(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'menuapp_recipe'
        unique_together = ['menu_item', 'ingredient']

    def __str__(self):
        return "menu_item: {0} - ingredient {1} - {2}".format(self.menu_item.__str__(),
                                                              self.ingredient.name, self.quantity)

    def as_dict(self):
        """
        Returns the object as a dictionary
        :return:
        """
        return {
            "menu_item": self.menu_item,
            "ingredient": self.ingredient,
            "quantity": self.quantity
        }

    def get_absolute_url(self):
        return reverse('recipe_list')

    def enough(self):
        """
        Checks if the ingredient quantity is enough to make the recipe
        :return:
        """
        return self.quantity <= self.ingredient.quantity


class Order(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'menuapp_order'
        ordering = ['order_date']

    def __str__(self):
        return "Menu item: {0} - Order date: {1}".format(self.menu_item.name, self.order_date)

    def get_absolute_url(self):
        """
        Returns the absolute url for the object
        :return:
        """
        return reverse('order_list')
