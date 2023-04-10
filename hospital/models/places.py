from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    state_code = models.CharField(max_length=2)


class Room(models.Model):
    pass


class Bed(models.Model):
    pass