from django.urls import path
from . import views

app_name = 'reservation'
urlpatterns = [
    path('', views.booking, name='booking'),
    path('my/', views.my_reservations, name='my_reservations'),
    path('cancel/<int:pk>/', views.cancel_reservation, name='cancel'),
    path('availability/', views.availability, name='availability'),
]
