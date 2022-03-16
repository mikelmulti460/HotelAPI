#Django
from django.contrib import admin

#Rooms
from rooms.models import Room, Booking

# Models registered.

admin.site.register(Room)
admin.site.register(Booking)