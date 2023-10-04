from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.IndexPage, name="index"),
    path("contactpage/", views.ContactPage, name="contact"),
    path("aboutus/", views.AboutPage, name="about"),
    path("menu/", views.MenuPage, name="menu"),
    #### RECIPE/RESTAURANT ####
    path('restaurants/', views.Restaurants.as_view(), name="restaurants"),
    path('restaurant/', views.Restaurants.as_view(), name="restaurant"),
    path('restaurantdetail/<str:pk>/', views.RestaurantDetail.as_view(), name="restaurantdetail"),
    path('restaurants/<str:restaurant_id>/recipes/', views.Recipe.as_view(), name="restaurant_recipe"),
    path('restaurants/<str:restaurant_id>/recipes/<str:recipe_id', views.RecipeDetail.as_view(), name="restaurant_recipe_detail"),
]