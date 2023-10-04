from django.shortcuts import render,redirect
from .models import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from rest_framework.views import APIView
from . import serializers
from django.http import Http404
from rest_framework import status

# Create your views here.
def IndexPage(request):
    return render(request, "peeps/index.html")

def ContactPage(request):
    return render(request, "peeps/contact.html")

def AboutPage(request):
    return render(request,"peeps/aboutus.html")

def MenuPage(request):
    return render(request, "peeps/menu.html")

class Restaurants(generics.CreateAPIView):
    
    renderer_classes = [TemplateHTMLRenderer]
    
    # def dispatch(self, request, *args, **kwargs):
    #     if request.method == 'GET':
    #         restaurants = Restaurant.objects.all()
    #         serializer = serializers.RestaurantSerializer(restaurants, many=True).data
    #         return Response({'restaurants':restaurants}, template_name='peeps/restaurants.html')
        
    #     elif request.method == 'POST':
    #         serializer = serializers.RestaurantSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.data, template_name = 'peeps/restaurant.html').dispatch(request, *args, **kwargs)
            
            
    
    def get(self, request):
        if request.method == 'GET':
            restaurants = Restaurant.objects.all()
            serializer = serializers.RestaurantSerializer(restaurants, many=True).data
            return Response({'restaurants':restaurants}, template_name='peeps/restaurants.html')
        # return Response({'restaurants':restaurants, 'serializer':serializer}, template_name = 'peeps/restaurant.html')
    
    def post(self, request):
        if request.method == 'POST':
            serializer = serializers.RestaurantSerializer(data=request.data)
        # queryset = self.get_queryset()
        # serializer = serializers.RestaurantSerializer(queryset)
        # name = request.data['name']
        # direction = request.data['direction']
        # phone = request.data['phone']
        # newres = Restaurant.objects.create(name=name, direction=direction, phone=phone)
            if serializer.is_valid():
                instance = serializer.save()
                instance.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED, template_name = 'peeps/restaurants.html')
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, template_name = 'peeps/restaurants.html')
        
    
class RestaurantDetail(generics.DestroyAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    
    
    def get(self, request, restaurant_id):
        try:
            restaurants = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Http404
        serializer = serializers.RestaurantSerializer(restaurants)
        # return Response(serializer.data)
        return Response({'serializer': serializer, 'restaurant':restaurants}, template_name = 'peeps/restaurant_detail.html')
    
    
    def delete(self, request, restaurant_id):
        # if request.method == 'POST':
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Http404
        restaurant.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return redirect('peeps/restaurant.html')
    
class Recipe(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_names = 'recipe.html'
    
    def get(self, request, restaurant_id):
        recipes = Recipe.objects.filter(restaurant_id=restaurant_id)
        serializer = serializers.RecipeSerializer(recipes, many=True)
        # return Response(serializer.data)
        return Response({'recipes':recipes, 'serializer':serializer})
        
    def post(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Http404
        
        serializer = serializers.RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant_id=restaurant_id, ingredients=request.data.get("ingredients"))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'restaurant':restaurant, 'serializer':serializer})
    
class RecipeDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_names = 'recipe_detail.html'
    
    def get(self, request, restaurant_id, recipe_id):
        try:
            recipes = Recipe.objects.get(restaurant_id=restaurant_id, pk=recipe_id)
        except Recipe.DoesNotExist:
            raise Http404
        serializer = serializers.RecipeSerializer(recipes)
        # return Response(serializer.data)
        return Response({'recipe':recipes, 'serializer':serializer})
    
    def delete(self, request, restaurant_id, recipe_id):
        try:
            recipe = Recipe.objects.get(restaurant_id=restaurant_id, pk=recipe_id)
        except Recipe.DoesNotExist:
            raise Http404
        recipe.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return redirect('recipe.html')