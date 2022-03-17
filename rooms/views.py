"""
Views for rooms
"""
#Rest Framework
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

#Rooms
from rooms.models import Room, Booking
from rooms.serializers import RoomSerializer, BookingSerializer

class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rooms to be viewed or edited.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def destroy(self, request, *args, **kwargs):
        """
        Override the destroy method to delete the room and all the bookings associated with it.
        """
        room = self.get_object()
        room.available = False
        room.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def list(self, request, *args, **kwargs):
        """
        This method handles the booking of rooms
        """
        #Get the room
        room = Room.objects.get(pk=kwargs['pk'])
        #Get the booking
        booking = room.booking_set.all()
        #Get the serializer
        serializer = BookingSerializer(booking, many=True)
        #Return the data
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Override the retrieve method to get the booking data for room
        """
        #Get the room
        pk_room=kwargs['pk_room']
        room = Room.objects.get(pk=pk_room)
        rooms = room.booking_set.all()
        #Get the booking
        instance = self.get_object()
        #Validate if the booking is for the room
        if instance in rooms:
            return Response(BookingSerializer(instance).data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        """
        This method handles the booking of rooms
        """
        #Get the room
        print(request)
        room = Room.objects.get(pk=kwargs['pk'])
        #Get the serializer
        serializer = BookingSerializer(data=request.data,context={'room':room, 'booking_id':None})
        #Validate the data
        if serializer.is_valid():
            #Create the booking
            booking = serializer.save(room=room)
            #Get the booking
            serializer = BookingSerializer(booking)
            #Return the data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Override the update method to get the booking data for room
        """
        #Get the room
        pk_room=kwargs['pk_room']
        room = Room.objects.get(pk=pk_room)
        rooms = room.booking_set.all()
        #Get the booking
        instance = self.get_object()
        #Validate if the booking is for the room
        if instance in rooms:
            #Get the serializer
            serializer = BookingSerializer(
                instance, data=request.data,
                context={'room':room, 'booking_id':instance.id}
            )
            #Validate the data
            if serializer.is_valid():
                #Update the booking
                serializer.save()
                #Return the data
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        """
        Override the destroy method to get the booking data for room
        """
        #Get the room
        pk_room=kwargs['pk_room']
        room = Room.objects.get(pk=pk_room)
        rooms = room.booking_set.all()
        #Get the booking
        instance = self.get_object()
        #Validate if the booking is for the room
        if instance in rooms:
            #Delete the booking
            instance.status = 3
            instance.save()
            #Return the data
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)