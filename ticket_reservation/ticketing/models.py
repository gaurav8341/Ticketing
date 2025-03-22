from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
# What do we need.


# 4. Train
#    id,
#    Name,
#    Source,
#    Destination,
#    starttime,
#    endtime,

# class Train(models.Model):
#     name = models.CharField(max_length=100)
#     source = models.CharField(max_length=100)
#     destination = models.CharField(max_length=100)
#     number_of_coaches = models.IntegerField()
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()

#     def __str__(self):
#         return self.name


# This will be created automatically.
# 2. Berth
#    id
#    Berth Type, Side lower, other # this can be a boolean field. but lets keep it open
#    TrainID
#    Booked 

class Berth(models.Model):
    BERTH_TYPES = [
        ('SL', 'Side Lower'),
        ('OTHER', 'Other'),# WE DONT HAVE TIME TO DECIDE NUMBER OF BERTHS FOR EACH TYPE
        # ('SU', 'Side Upper'),
        # ('LB', 'Lower Berth'),
        # ('MB', 'Middle Berth'),
        # ('UB', 'Upper Berth'),
    ]
    berth_type = models.CharField(max_length=2, choices=BERTH_TYPES)
    berth_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(63)])
    # train = models.ForeignKey(Train, on_delete=models.CASCADE)
    # coach_number = models.IntegerField()])
    booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_berth_type_display()} - {self.berth_number}"


# 3. Passenger -- This is not user
#    id,
#    Name,
#    Age, # This will be at the time of journey 
#    GuardianID, self foreign key for children less than 5
#    TicketID

class Passenger(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    guardian = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    details = models.JSONField()
    
    def __str__(self):
        return self.name

# 1. tickets
#    id
#    Ticket type RAC, Confirmed, Waiting List
#    Active
#    PassengerID
#    Json -- Let it be here
#    BerthID,
#    TrainID
#    BookingTime 
#    

class Ticket(models.Model):
    TICKET_TYPES = [
        ('RAC', 'Reservation Against Cancellation'),
        ('CNF', 'Confirmed'),
        ('WL', 'Waiting List'),
    ]
    ticket_type = models.CharField(max_length=3, choices=TICKET_TYPES)
    active = models.BooleanField(default=True)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    berth = models.ForeignKey(Berth, on_delete=models.CASCADE)
    # train = models.ForeignKey(Train, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    details = models.JSONField()

    def __str__(self):
        return f"{self.get_ticket_type_display()} - {self.passenger.name}"