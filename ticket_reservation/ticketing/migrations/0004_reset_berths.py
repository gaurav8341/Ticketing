from django.db import migrations, models
from ticketing.models import Berth, Passenger, Ticket

def reset_berths(apps, schema_editor):
    berth_structure = ['SL', 'LB', 'MB', 'UB', 'LB', 'MB', 'UB']

    berth_number = 1
    berths = []
    
    Berth.objects.all().update(Active=False)
    
            
    # Deactivate all tickets related to inactive berths
    Ticket.objects.filter(BerthID__Active=False).update(Active=False)
    
    # Deactivate all passengers linked to inactive tickets
    Passenger.objects.filter(Active=True).update(Active=False)

    
    print('Successfully deactivated all berths')
    
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
    
    print('Successfully created 63 berths')

class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0003_alter_passenger_details_alter_ticket_details'),
    ]

    operations = [
        migrations.RunPython(reset_berths),
    ]