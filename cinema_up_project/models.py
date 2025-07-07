import os

from django.db import models
from django.utils.text import slugify

from main import settings


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def play_image_upload_path(instance, filename):
        ext = filename.split(".")[-1]
        filename = f"uploaded-{slugify(instance.title)}.{ext}"
        return os.path.join("plays/", filename)


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


def play_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"uploaded-{slugify(instance.title)}.{ext}"
    return os.path.join("plays/", filename)


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.ManyToManyField("Genre", related_name="plays")
    actors = models.ManyToManyField("Actor", related_name="plays")
    image = models.ImageField(upload_to=play_image_upload_path, blank=True, null=True)

    def __str__(self):
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @property
    def capacity(self):
        return self.rows * self.seats_in_row


class Performance(models.Model):
    play = models.ForeignKey(
        Play, on_delete=models.CASCADE, related_name="performances"
    )
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.CASCADE, related_name="performances"
    )
    show_time = models.DateTimeField()

    class Meta:
        ordering = ["-show_time"]

    def __str__(self):
        return f"{self.play.title} - {self.play.theatre_hall} at {self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reservation #{self.id} by {self.user}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        ordering = ["row", "seat"]
        unique_together = ("row", "seat", "performance")

    def __str__(self):
        return (f"Ticket for {self.performance} "
                f"Row {self.row}, "
                f"Seat {self.seat}"
                )
