from django.utils.timezone import now
from .models import *

def release_expired_seats():
    expired_reservations = Reservations.objects.filter(end_time__lte=now(), status='Confirmed')#数据量大的话查的太多 数据量很难大
    for reservation in expired_reservations:
        seat = Seats.objects.get(seat_id=reservation.seat_id)
        seat.status = 'Available'
        seat.save()
        reservation.status = 'Completed'
        reservation.save()
