# filepath: /home/vast/repos/Ticketing/ticket_reservation/ticketing/management/commands/create_berths.py
from django.core.management.base import BaseCommand
from ticketing.models import Berth, Ticket, Passenger

class Command(BaseCommand):
    help = 'Create initial berths in the Berth table and Deactivate older berths of any. This will also deactivate the tickets and passengers associated with the berths'

    def handle(self, *args, **kwargs):
        berth_structure = ['SL', 'LB', 'MB', 'UB', 'LB', 'MB', 'UB']

        berth_number = 1
        berths = []
        
        Berth.objects.all().update(Active=False)
        
                
        # Deactivate all tickets related to inactive berths
        Ticket.objects.filter(BerthID__Active=False).update(Active=False)

        # Deactivate all passengers linked to inactive tickets
        Passenger.objects.filter(Ticket__Active=False).update(Active=False)

        
        self.stdout.write(self.style.SUCCESS('Successfully deactivated all berths'))
        
        for compartment in range(9):  # 9 compartments
            for berth_type in berth_structure:
                b = Berth(
                    Type=berth_type,
                    BerthNumber=berth_number,
                    Active=True,
                    Booked=False
                )
                berths.append(b)
                berth_number += 1

        Berth.objects.bulk_create(berths) 
        
        self.stdout.write(self.style.SUCCESS('Successfully created 63 berths'))