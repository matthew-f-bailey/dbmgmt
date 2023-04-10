from django.db import models


class Clinic(models.Model):
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=254)

# unit in clinc
class Unit(models.Model):
    name = models.CharField(max_length=254)
    clinic = models.ForeignKey(
        Clinic,
        on_delete =  models.CASCADE
    )

# room inside unit
class Room(models.Model):
    number = models.IntegerField()
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE
    )

# bed in a room
class Bed(models.Model):
    bedLetter = models.CharField(max_length=30)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE
    )
