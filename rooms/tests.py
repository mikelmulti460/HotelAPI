""" Test for the rooms API """
#Django
import datetime
from django.urls import reverse

#Django rest framework
from rest_framework.test import APITestCase
from rest_framework import status

#Rooms
from rooms.models import Room, Booking

class ModelsCreationTest(APITestCase):
    """ Test the rooms models """
    def setUp(self):
        """ Create the room and booking """
        self.room = Room.objects.create(number='101', description='Room for testing', beds=2, price=100.0, available=True)
        self.booking = Booking.objects.create(
            first_name="John",
            last_name="Doe",
            email="jhondoe@example.com",
            phone="+51999999999",
            document_number="99999999999",
            check_in=datetime.date.today(),
            check_out=datetime.date.today() + datetime.timedelta(days=1),
            total_days=1,
            ammount_paid=100.00,
            paid_method="cash",
            room=self.room,
            status=1
            )

    def test_create_room(self):
        """ Test the creation of a room """
        url = reverse('rooms:room-list')
        data = { 'number': '201', 'description': 'Room for testing', 'beds': 2, 'price': 100.0, 'available': True }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_booking(self):
        """ Test the creation of a booking """
        url = reverse('rooms:booking-list', kwargs={'pk': self.room.pk})
        data = { 
            "first_name": "John",
            "last_name": "Doe",
            "email": "email@example.com",
            "phone": "922298917",
            "document_number": 42859163,
            "check_in": datetime.date.today()+datetime.timedelta(days=365),
            "check_out": datetime.date.today()+datetime.timedelta(days=368),
            "paid_method": "Efectivo",
            "status": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['total_days'], 3)
        self.assertEqual(response.json()['ammount_paid'], '300.00')
    
    
    def test_modify_booking(self):
        """ Test the modification of a booking """
        url = reverse('rooms:booking-detail', kwargs={'pk_room': self.room.pk, 'pk': self.room.booking_set.first().pk})
        data = { 
            "first_name": "Linus",
            "last_name": "Torvalds",
            "email": "Linux@gnu.com",
            "phone": "945418185",
            "document_number": 27858018,
            "check_in": datetime.date.today()+datetime.timedelta(days=2),
            "check_out": datetime.date.today()+datetime.timedelta(days=4),
            "paid_method": "Efectivo",
            "status": 2
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['total_days'], 2)
        self.assertEqual(response.json()['ammount_paid'], '200.00')
    
    def test_delete_booking(self):
        """ Test the deletion of a booking """
        url = reverse('rooms:booking-detail', kwargs={'pk_room': self.room.pk, 'pk': self.room.booking_set.first().pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url, format='json')
        self.assertEqual(response.json()['status'], 3)
    
    def test_delete_room(self):
        """ Test the deletion of a room """
        url = reverse('rooms:room-detail', kwargs={'pk': self.room.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(url, format='json')
        self.assertEqual(response.json()['available'], False)
