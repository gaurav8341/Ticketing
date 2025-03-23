from django.shortcuts import render

from django.views import View
from django.http import JsonResponse
from django.db import transaction

import json

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
    
    @transaction.atomic
    def book_ticket(self, request):
                
        # book a ticket. 
        # this thing does not handle multiple passengers at the same time.
        # It will handle infants and passengers though.
        # You can book one ticket at a time through this call 

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

        # data = request.POST
        data = json.loads(request.body)
        passenger_name = data.get('passenger_name')
        passenger_age = int(data.get('passenger_age', 0))
        infants = data.get('infants', [])
        gender = data.get('gender') # will only accept M, F, O
        
        main_passenger = Passenger(Name=passenger_name, Age=passenger_age, Gender=gender)
        infant_passengers = []
        for infant in infants:
            # check Age of infant
            if int(infant.get('passenger_age', 0)) > 5:
                return JsonResponse({'error': 'Infant age should be less than 5'}, status=400)        
        
        priority_booking = False
        berth = None
        ticket_availability = ''
        rac_berth_count = 0
        if (gender == 'F' and len(infants) > 0) or (passenger_age > 60):
            # priority booking
            # I am making assumption that side lower berth and lower berth is diiferent
            berth = Berth.objects.filter(Active=True, Booked=False, Type ='LB').order_by("BerthNumber").select_for_update().first()
            
            if berth:
                priority_booking = True
                ticket_availability = 'CNF'
            else:
                priority_booking = False
        
        if not priority_booking:
            # try:
                # dont select SL berth here
            berth = Berth.objects.exclude(Type__in = ['SL', 'LB']).filter(Active=True, Booked=False,).order_by("BerthNumber").select_for_update().first()
            if not berth:
                # check for lb
                berth = Berth.objects.filter(Active=True, Booked=False, Type='LB').order_by("BerthNumber").select_for_update().first()
                
            if not berth:
                wl_tickets_count = Ticket.objects.filter(Type='WL', Active=True).count()
                rac_tickets_count = Ticket.objects.filter(Type='RAC', Active=True).count()
                
                if wl_tickets_count >= 10 and rac_tickets_count >= 18:
                    ticket_availability = 'not_available'
                elif wl_tickets_count < 10 and rac_tickets_count >= 18:
                    ticket_availability = 'WL'
                elif wl_tickets_count < 10 and rac_tickets_count < 18:
                    ticket_availability = 'RAC'
            else:
                ticket_availability = 'CNF'

        
        if ticket_availability == 'not_available':
            return JsonResponse({'error': 'No ticket available'}, status=400)
            # create ticket without berth
        elif ticket_availability == 'RAC':
            # find a berth and create ticket
            berth = Berth.objects.filter(Active=True, Booked=False,Type='SL').order_by("BerthNumber").select_for_update().first()
            
            if not berth:
                return JsonResponse({'error': 'No ticket available'}, status=400)
            
            # just double check there are not more than one RAC ticket for the same berth
            rac_tickets = Ticket.objects.filter(Type='RAC', Active=True, BerthID=berth).count()
            if rac_tickets > 1:
                return JsonResponse({'error': 'No ticket available'}, status=400)
            rac_berth_count = rac_tickets + 1
        
        # we have berth now
        
        # create main passenger ticket
        main_passenger.save()
        
        infant_passengers = []
        for infant in infants:            
            infant_passengers.append(Passenger(Name=infant.get('passenger_name'), Age=infant.get('passenger_age'), Guardian=main_passenger))
        
        Passenger.objects.bulk_create(infant_passengers)
        
        ticket = Ticket(Type=ticket_availability, PassengerID=main_passenger)
        
        if berth:
            ticket.BerthID = berth
            if (ticket_availability == 'RAC' and rac_berth_count == 2) or ticket_availability == 'CNF':
                berth.Booked = True
                berth.save()
        
        ticket.save()  
        
        ticket_details = {
            'ticket_id': ticket.id,
            'ticket_type': ticket.Type,
            'berth_number': ticket.BerthNumber if ticket.BerthNumber else 'NA',
            'berth_type': ticket.BerthType if ticket.BerthType else 'NA'
        }      
        
        return JsonResponse(ticket_details)
    
    @transaction.atomic
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
        
        data = json.loads(request.body)
        ticket_id = int(data.get('ticket_id', None))
        
        if not ticket_id:
            return JsonResponse({'error': 'Ticket ID is required'}, status=400)
        
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return JsonResponse({'error': 'No Such Ticket Available'}, status=400)
        ticket.Active = False
        ticket.save()
        
        if ticket.Type == 'RAC':
            # check if there is any waiting list
            wl_ticket = Ticket.objects.filter(Type='WL', Active=True).order_by("BookingTime").first()
            
            berth = Berth.objects.filter(id = ticket.BerthID.id).select_for_update().first()
            
            if wl_ticket: 
                wl_ticket.Type = 'RAC'
                wl_ticket.BerthID = berth
                # wl_ticket.Active = False
                wl_ticket.save()
                # send the update to the passenger that his ticket is confirmed
            else:
                berth.Booked = False
                berth.save()
                
            return JsonResponse({'message': 'Ticket cancelled'})
        elif ticket.Type == 'CNF':

            rac_ticket = Ticket.objects.filter(Type='RAC', Active=True).order_by("BookingTime").first()
            
            berth = Berth.objects.filter(id = ticket.BerthID.id).select_for_update().first()
            
            if rac_ticket: 
                rac_ticket.Type = 'CNF'
                rac_ticket.BerthID = berth
                # rac_ticket.BerthType = wl_ticket.BerthType
                # wl_ticket.Active = False
                rac_ticket.save()
                # send the update to the passenger that his ticket is confirmed
            else:
                berth.Booked = False
                berth.save()
            
            return JsonResponse({'message': 'Ticket cancelled'})
        else:
            # check if there is any waiting list
            return JsonResponse({'message': 'Ticket cancelled'})    
    
    def booked_tickets(self, request):
        # Booked Tickets
        """
        1. Show all the booked tickets
        2. Show the details of the ticket
        3. Show the passenger details
        4. Show the berth details
        """
        
        tickets = Ticket.objects.filter(Active=True)
        ticket_list = []        
        
        for ticket in tickets:
            infants = Passenger.objects.filter(Guardian=ticket.PassengerID)
            infant_list = []
            for infant in infants:
                infant_list.append({
                    'passenger_name': infant.Name,
                    'passenger_age': infant.Age
                })
            ticket_list.append({
                'ticket_id': ticket.id,
                'passenger_name': ticket.PassengerID.Name,
                'passenger_age': ticket.PassengerID.Age,
                'passenger_gender': ticket.PassengerID.Gender,
                'berth_type': ticket.BerthType,
                'infants': infant_list,
                'berth_number': ticket.BerthNumber,
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
   