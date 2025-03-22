from django import forms
from .models import Passenger, Ticket

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['Name', 'Age', 'Guardian']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['Type', 'Details']