from django.db import models


# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'menuapp_menuitem'

    def __str__(self):
        return "{0} - Description: {1} - Price: {2}".format(self.name, self.description, self.price)

    def get_absolute_url(self):
        return "/menu"


class Ingredient(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    unit = models.CharField(max_length=50)
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'menuapp_ingredient'

    def __str__(self):
        return {
            "name": self.name,
            "description": self.description,
            "unit": self.unit,
            "price_per_unit": self.price_per_unit,
            "quantity": self.quantity,
        }

    def get_absolute_url(self):
        return "/ingredients"


class Recipe(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'menuapp_recipe'

    def __str__(self):
        return "menu_item: {0} - ingredient {1} - {2}".format(self.menu_item.__str__(),
                                                              self.ingredient.name, self.quantity)

    def get_absolute_url(self):
        return "/menu"

    def enough(self):
        return self.quantity <= self.ingredient.quantity


class Order(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'menuapp_order'
        ordering = ['order_date']

    def __str__(self):
        return f"menu_item=[{self.menu_item.__str__()}]; time={self.order_date}"

    def get_absolute_url(self):
        return "/purchases"
