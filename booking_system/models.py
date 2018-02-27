from django.db import models


class Room(models.Model):
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)
    name = models.CharField(max_length=64)

class Reservation(models.Model):
    date = models.DateField(unique=True)
    room_booked = models.ManyToManyField(Room)



