from django.shortcuts import render

from django.views import View
from django.http import JsonResponse

from .models import Berth, Passenger, Ticket


# Create your views here.
class TicketingView(View):
    def dispatch(self, request, *args, **kwargs):
        #    return super().dispatch(request, *args, **kwargs)
        action = kwargs.get('action')
        if action == 'book':
            if request.method == 'POST':
                return self.book_ticket(request)
        elif action == 'cancel':
            if request.method == 'POST':
                return self.cancel_ticket(request)
        elif action == 'booked':
            if request.method == 'GET':
                return self.booked_tickets(request)
        elif action == 'available':
            if request.method == 'GET':
                return self.available_berths(request)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
    
    def book_ticket(self, request):
                
        # book a ticket. 

        """ 
        1. Get passenger details from user
        2. Get train details from user -- optional
        3. Check the availability of berth
        4. If no availability the send a message to user
        5. If available then book the ticket
        4. Take control of the berth record.
        5. Allocate berth to passenger if it is available
        6. Send the ticket details to user
        """

        data = request.POST
        passenger_name = data.get('passenger_name')
        passenger_age = data.get('passenger_age')
        berth_type = data.get('berth_type')
        berth_number = data.get('berth_number')
        ticket_type = data.get('ticket_type')
        
        passenger = Passenger.objects.create(Name=passenger_name, Age=passenger_age)
        berth = Berth.objects.get(BerthType=berth_type, BerthNumber=berth_number)
        ticket = Ticket.objects.create(Type=ticket_type, PassengerID=passenger, BerthID=berth)
        
        return JsonResponse({'ticket_id': ticket.id})
    
    def cancel_ticket(self, request):
        # Cancel a ticket.

        """
        1. Get the ticket details from user
        2. Check the ticket details
        3. If the ticket is not found then send a message to user
        4. If the ticket is found then cancel the ticket
        5. Check for any waiting list
        6. If there is any waiting list then allocate the berth to the waiting list
        7. Send the message to the user
        8. if there is no waiting list then make the berth available
        """
        
        data = request.POST
        ticket_id = data.get('ticket_id')
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.delete()
        return JsonResponse({'message': 'Ticket cancelled'})    
    
    def booked_tickets(self, request):
        # Booked Tickets
        """
        1. Show all the booked tickets
        2. Show the details of the ticket
        3. Show the passenger details
        4. Show the berth details
        """
        
        tickets = Ticket.objects.all()
        ticket_list = []        
        
        for ticket in tickets:
            ticket_list.append({
                'ticket_id': ticket.id,
                'passenger_name': ticket.PassengerID.Name,
                'passenger_age': ticket.PassengerID.Age,
                'berth_type': ticket.BerthType,
                'berth_number': ticket.BerthID.BerthNumber,
                'ticket_type': ticket.Type
            })
        
        return JsonResponse({'tickets': ticket_list})
    
    def available_berths(self, request):
        
        # Avilable berths
        """
        1. Show all the available berths
        2. Show the details of the berth
        """
        
        berths = Berth.objects.filter(Active=True, Booked=False)
        berth_list = []
        
        for berth in berths:
            berth_list.append({
                'berth_type': berth.Type,
                'berth_number': berth.BerthNumber
            })
        
        return JsonResponse({'berths': berth_list})
   