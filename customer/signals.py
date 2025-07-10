# hotel/signals.py
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from datetime import timedelta

from hotel.models import *
from .models import *







def update_availability(room, start_date, end_date, delta):
    date = start_date
    while date < end_date:
        obj, _ = RoomAvailability.objects.get_or_create(room=room, date=date)
        obj.available_count = max(obj.available_count + delta, 0)
        obj.save()
        date += timedelta(days=1)


@receiver(pre_save, sender=HotelBooking)
def handle_old_booking(sender, instance, **kwargs):
    if instance.pk:
        old = HotelBooking.objects.get(pk=instance.pk)
        instance._old_check_in = old.check_in
        instance._old_check_out = old.check_out
        instance._old_room = old.room
    else:
        instance._old_check_in = None
        instance._old_check_out = None
        instance._old_room = None


@receiver(post_save, sender=HotelBooking)
def handle_new_booking(sender, instance, created, **kwargs):
    if instance.status == 'cancelled':
        return  # Don't reduce count for cancelled

    if created:
        update_availability(instance.room, instance.check_in, instance.check_out, delta=-1)
    else:
        # Restore old only if it wasn't cancelled
        if instance._old_check_in and instance._old_check_out and instance._old_room:
            old = HotelBooking.objects.get(pk=instance.pk)
            if old.status != 'cancelled':
                update_availability(old.room, old.check_in, old.check_out, delta=+1)

        # Apply new only if current is not cancelled
        update_availability(instance.room, instance.check_in, instance.check_out, delta=-1)


@receiver(pre_delete, sender=HotelBooking)
def handle_deleted_booking(sender, instance, **kwargs):
    if instance.status != 'cancelled':
        update_availability(instance.room, instance.check_in, instance.check_out, delta=+1)

