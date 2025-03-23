import json

from django.test import TestCase, Client
from django.urls import reverse

from .models import Berth, Passenger, Ticket
from .utils import reset_berths

class TicketingViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.book_url = reverse('ticketing', kwargs={'action': 'book'})
        self.cancel_url = reverse('ticketing', kwargs={'action': 'cancel'})
        self.booked_url = reverse('ticketing', kwargs={'action': 'booked'})
        self.available_url = reverse('ticketing', kwargs={'action': 'available'})

        # Create test data
        reset_berths()
        # self.passenger = Passenger.objects.create(Name='John Doe', Age=30)
        # self.berth = Berth.objects.create(Type='LB', BerthNumber=1, Booked=False, Active=True)
        # self.ticket = Ticket.objects.create(Type='CNF', Active=True, PassengerID=self.passenger, BerthID=self.berth)

    def test_book_ticket_post(self):
        data = {
            'passenger_name': 'Jane Doe',
            'passenger_age': 25,
            'infants': [],
            'gender': 'M'
        }
        response = self.client.post(self.book_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertIn('ticket_type', response.json())
        self.assertEqual('CNF', resp_data['ticket_type'])
        self.assertIn('berth_number', response.json())
        self.assertEqual(3, int(resp_data['berth_number']))
        self.assertIn('berth_type', response.json())
        self.assertEqual('MB', resp_data['berth_type'])

    def test_priority_booking_post(self):
        data = {
            'passenger_name': 'Jane Doe',
            'passenger_age': 25,
            'infants': [{
                    "passenger_name":"son",
                    "passenger_age": 4,
                    "gender": 'M'
                }],
            'gender': 'F'
        }
        response = self.client.post(self.book_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertIn('ticket_type', response.json())
        self.assertEqual('CNF', resp_data['ticket_type'])
        self.assertIn('berth_number', response.json())
        self.assertEqual(2, int(resp_data['berth_number']))
        self.assertIn('berth_type', response.json())
        self.assertEqual('LB', resp_data['berth_type'])
        
        
        data = {
            'passenger_name': 'Jane Doe',
            'passenger_age': 65,
            'infants': [],
            'gender': 'F'
        }
        response = self.client.post(self.book_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        resp_data = response.json()
        self.assertIn('ticket_type', response.json())
        self.assertEqual('CNF', resp_data['ticket_type'])
        self.assertIn('berth_number', response.json())
        self.assertEqual(5, int(resp_data['berth_number']))
        self.assertIn('berth_type', response.json())
        self.assertEqual('LB', resp_data['berth_type'])

    def test_booking_cancellation_post(self):
        
        data = {
            'passenger_name': 'Jane Doe',
            'passenger_age': 25,
            'infants': [{
                    "passenger_name":"son",
                    "passenger_age": 4,
                    "gender": 'M'
                }],
            'gender': 'F'
        }
        # print(data)
        response = self.client.post(self.book_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = {
            "ticket_id": response.json()["ticket_id"]
        }
        response = self.client.post(self.cancel_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Ticket cancelled", response.json()["message"])
        
        data = {
            "ticket_id": 4567890
        }
        response = self.client.post(self.cancel_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual("No Such Ticket Available", response.json()["error"])
    
    def test_available_berths_get(self):
        response = self.client.get(self.available_url)
        self.assertEqual(response.status_code, 200)
        # self.assertIn('berths', response.json())
        self.assertGreaterEqual(len(response.json()['berths']), 63)
        
        data = {
            'passenger_name': 'Jane Doe',
            'passenger_age': 25,
            'infants': [{
                    "passenger_name":"son",
                    "passenger_age": 4,
                    "gender": 'M'
                }],
            'gender': 'F'
        }
        # print(data)
        response = self.client.post(self.book_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(self.available_url)
        self.assertEqual(response.status_code, 200)
        # self.assertIn('berths', response.json())
        self.assertGreaterEqual(len(response.json()['berths']), 62)
    
    def test_booked_berths_get(self):
        
        data = {
            'passenger_name': 'Jane Doe',
            'passenger_age': 25,
            'infants': [{
                    "passenger_name":"son",
                    "passenger_age": 4,
                    "gender": 'M'
                }],
            'gender': 'F'
        }
        # print(data)
        response = self.client.post(self.book_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(self.booked_url)
        self.assertEqual(response.status_code, 200)
        # self.assertIn('berths', response.json())
        self.assertGreaterEqual(len(response.json()['tickets']), 1)
        
        
        
