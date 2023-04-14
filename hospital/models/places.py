from django.db import models


class Clinic(models.Model):
    # See TODO below about this...
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=254)

# unit in clinc
class Unit(models.Model):
    name = models.CharField(max_length=254)
    # Allows beds and rooms to be uniquely id'd by name
    prefix = models.CharField(max_length=3)

    # TODO: Do we want to support multiple clinics? Or is the
    # whole hospital app the clinic? If we do this, then people
    # also need to be assigned a clinic along with almost every
    # other entity we create. Would require everything
    # inheriting some model w/ clinic as foriegn key
    # clinic = models.ForeignKey(
    #     Clinic,
    #     on_delete=models.CASCADE
    # )

    def __str__(self) -> str:
        return f"{self.name} ({self.prefix})"


class Room(models.Model):
    """ A room inside a unit """
    number = models.PositiveIntegerField()
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.unit.prefix}-{self.number}"

class BedManager(models.Manager):
    """ Allows for lookup by bed_code
    """
    def get_bed_by_code(self, code):
        """
            Allows the following method on objects
            Bed.objects.get_room_by_code('icu-9A')
        """
        room = [r for r in self.get_queryset().all() if r.bed_code==code]
        if not room:
            # Return None if no bed found
            return None
        return room[0]


class Bed(models.Model):
    """ Beds can id unit, room and bed """
    bed_letter = models.CharField(max_length=1)
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )
    objects = BedManager()

    @property
    def bed_code(self):
        """ Bed manager used to search by this since should be unique
        If not, will return first one, but should be unique
        """
        return f"{self.room.unit.prefix}-{self.room.number}{self.bed_letter}"

    def __str__(self) -> str:
        return self.bed_code