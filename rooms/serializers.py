""" Serializers for the rooms API module. """
#Python
import datetime

#RestFramework
from rest_framework import serializers

#rooms
from rooms.models import Room, Booking

class RoomSerializer(serializers.ModelSerializer):
    """
    Serializer for Room model
    """
    class Meta:
        """ Meta class for RoomSerializer """
        model = Room
        fields = ('id', 'number', 'description', 'beds', 'price', 'available')

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model
    """
    class Meta:
        """ Meta class for BookingSerializer """
        model = Booking
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'document_number',
            'check_in',
            'check_out',
            'total_days',
            'ammount_paid',
            'paid_method',
            'room',
            'status',
        )
        read_only_fields = ('total_days', 'ammount_paid', 'room')

    def validate_check_in(self, value):
        """
        Validate the check in date
        """
        if value < datetime.date.today():
            raise serializers.ValidationError("Check-in must be today or a future date")
        return value

    def validate(self, data):
        """
        Validate the data
        """
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out must be after check-in")
        #Check if the room is available
        if not self.context['room'].available:
            raise serializers.ValidationError("This room is not available")
        #Check if the room is available for the dates
        if not (self.context['room'].available_for_dates(data['check_in'],
        data['check_out'], self.context['booking_id'])):
            raise serializers.ValidationError("This room is not available for those dates")

        return data

    def create(self, validated_data):
        """
        Create and return a new booking instance, given the validated data.
        """
        booking = Booking.objects.create(**validated_data)
        booking.total_days = booking.get_total_days()
        booking.ammount_paid = booking.get_total_price()
        booking.save()
        return booking

    def update(self, instance, validated_data):
        """
        Update and return an existing booking instance, given the validated data.
        """
        instance.check_in = validated_data.get('check_in', instance.check_in)
        instance.check_out = validated_data.get('check_out', instance.check_out)
        instance.total_days = instance.get_total_days()
        instance.ammount_paid = instance.get_total_price()
        return super().update(instance, validated_data)
    
