# -*- coding: utf-8 -*-
"""
URLs for rooms.
"""
# Django
from django.urls import include, path

# django-rest-framework
from rest_framework import routers

# Rooms
from rooms.views import RoomViewSet, BookingViewSet

app_name = 'rooms'
ROUTER = routers.DefaultRouter()
ROUTER.register(r'', RoomViewSet, basename='room')

urlpatterns = [
    path('', include(ROUTER.urls), name='room'),
    path('<int:pk>/booking/', BookingViewSet.as_view({'get': 'list', 'post': 'create'}), name='booking-list'),
    path('<int:pk_room>/booking/<int:pk>/', BookingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='booking-detail'),
]