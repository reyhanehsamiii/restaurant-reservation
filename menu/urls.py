from django.urls import path
from . import views

app_name = 'menu'
urlpatterns = [
    path('', views.menu_list, name='menu'),
    path('dish/<int:pk>/', views.dish_detail, name='dish_detail'),
    path('category/<str:cat>/', views.menu_list, name='category'),
    path('meal/<str:meal>/', views.menu_list, name='meal'),
    path('tag/<str:tag>/', views.menu_list, name='tag'),
    path('search/', views.search, name='search'),
]
