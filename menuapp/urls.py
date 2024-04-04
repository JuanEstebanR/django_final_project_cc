from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.MenuListView.as_view(), name='menu_list'),
    path('ingredients/', views.IngredientListView.as_view(), name='ingredient_list'),
    path('ingredient/create', views.IngredientCreateView.as_view(), name='ingredient_create'),
    path('ingredient/update/<int:pk>', views.IngredientUpdateView.as_view(), name='ingredient_update'),
    path('item/create', views.MenuItemCreateView.as_view(), name='menu_item_create'),
    path('recipe/create', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe_list'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order/create', views.OrderCreateView.as_view(), name='order_create'),
    path("signup/", views.SignUp.as_view(), name="signup"),
]