# filepath: /home/vast/repos/Ticketing/ticket_reservation/ticketing/management/commands/create_berths.py
from django.core.management.base import BaseCommand
from ticketing.models import Berth

class Command(BaseCommand):
    help = 'Create initial berths in the Berth table and Deactivate older berths of any. This will also deactivate the tickets and passengers associated with the berths'

    def handle(self, *args, **kwargs):
        berth_structure = ['SL', 'LB', 'MB', 'UB', 'LB', 'MB', 'UB']

        berth_number = 1
        berths = []
        
        Berth.objects.all().update(Active=False)
        Berth.objects.filter(Active=False).update(tickets__Active=False, tickets__passenger__active=False)
        
        self.stdout.write(self.style.SUCCESS('Successfully deactivated all berths'))
        
        for compartment in range(9):  # 9 compartments
            for berth_type in berth_structure:
                b = Berth(
                    berth_type=berth_type,
                    berth_number=berth_number,
                    Active=True,
                    booked=False
                )
                berths.append(b)
                berth_number += 1

        Berth.objects.bulk_create(berths) 
        
        self.stdout.write(self.style.SUCCESS('Successfully created 63 berths'))