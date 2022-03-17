""" Models from rooms module. """

from django.db import models


class Room(models.Model):
    """
    This is the custom model for rooms

    Attributes:
        number (int): The room number.
        description: The description of the room
        beds (int): The number of beds in the room
        price (float): The price of the room (per night)
        available (bool): The availability of the room
    """
    number = models.IntegerField(unique=True)
    description = models.TextField()
    beds = models.IntegerField()
    price = models.DecimalField(max_digits=8,decimal_places=2)
    available = models.BooleanField(default=True)

    def available_for_dates(self, check_in, check_out, booking_id=None):
        """
        This method checks if the room is available for the dates
        """
        if self.available:
            #Check if the room is available for the dates
            bookings = self.booking_set.all()
            for booking in bookings:
                if booking.id != booking_id:
                    if (booking.check_in <= check_in <= booking.check_out
                        or booking.check_in <= check_out <= booking.check_out):
                        return False
            return True
        return False

    def __str__(self):
        return self.description


class Booking(models.Model):
    """
    This is the custom model for bookings

    Atributes:
        first_name (str): The first name of the customer
        last_name (str): The last name of the customer
        email (str): The email of the customer
        phone (str): The phone number of the customer
        document_number (str): The document number of the customer
        room (Room): The room of the booking
        check_in (date): The check in date
        check_out (date): The check out date
        total_days (int): The total days of the booking
        ammount_paid (float): The ammount paid of the booking
        paid_method (str): The paid method of the booking
        status (str): The status of the booking
    """
    PENDING = 1
    PAID = 2
    DELETED = 3
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
        (DELETED, 'Deleted'),
    )
    #client data
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    document_number = models.IntegerField()
    #Room Data
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_days = models.IntegerField(default=0)
    ammount_paid = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    paid_method = models.CharField(max_length=50, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.room.description}"

    def get_total_days(self):
        """
        This method calculates the total days of the booking
        """
        return (self.check_out - self.check_in).days

    def get_total_price(self):
        """
        This method calculates the total price of the booking
        """
        return self.room.price * (self.check_out - self.check_in).days
