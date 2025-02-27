# polls/forms.py
from django import forms
from .models import Reservations

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = ['seat', 'start_time', 'end_time']

    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
