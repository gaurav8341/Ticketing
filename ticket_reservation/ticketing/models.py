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
        # ('OTHER', 'Other'),# WE DONT HAVE TIME TO DECIDE NUMBER OF BERTHS FOR EACH TYPE
        # ('SU', 'Side Upper'),
        ('LB', 'Lower Berth'),
        ('MB', 'Middle Berth'),
        ('UB', 'Upper Berth'),
    ]
    Type = models.CharField(max_length=2, choices=BERTH_TYPES)
    BerthNumber = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(63)])
    # train = models.ForeignKey(Train, on_delete=models.CASCADE)
    # coach_number = models.IntegerField()])
    Booked = models.BooleanField(default=False)
    Active = models.BooleanField(default=True)
    
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_Type_display()} - {self.BerthNumber}"


# 3. Passenger -- This is not user
#    id,
#    Name,
#    Age, # This will be at the time of journey 
#    GuardianID, self foreign key for children less than 5
#    TicketID

class Passenger(models.Model):
    Name = models.CharField(max_length=100)
    Age = models.IntegerField()
    Guardian = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    # Ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='passengers')
    Gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F','Female'), ('O', 'Other')], blank=True, null=True)
    Active = models.BooleanField(default=True)
    Details = models.JSONField()
    
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.Name

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
    Type = models.CharField(max_length=3, choices=TICKET_TYPES)
    Active = models.BooleanField(default=True)
    PassengerID = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name="tickets")
    BerthID = models.ForeignKey(Berth, on_delete=models.CASCADE, related_name='tickets', blank=True, null=True)
    BerthType = models.CharField(max_length=2, choices=Berth.BERTH_TYPES, blank=True, null=True) # This is for easy access
    BerthNumber = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(63)], blank=True, null=True) # This is for easy access
    # train = models.ForeignKey(Train, on_delete=models.CASCADE)
    BookingTime = models.DateTimeField(auto_now_add=True)
    Details = models.JSONField()
    
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.BerthID:
            self.BerthType = self.BerthID.Type
            self.BerthNumber = self.BerthID.BerthNumber
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_Type_display()} - {self.PassengerID.Name}"


