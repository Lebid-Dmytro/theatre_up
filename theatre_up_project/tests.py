from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from .models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket
)


class ModelTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Трагедія")
        self.actor = Actor.objects.create(
            first_name="Іван",
            last_name="Франко"
        )
        self.hall = TheatreHall.objects.create(
            name="Зала 1",
            rows=5,
            seats_in_row=10
        )
        self.play = Play.objects.create(
            title="Гамлет",
            description="Опис"
        )
        self.play.genres.add(self.genre)
        self.play.actors.add(self.actor)
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=timezone.now() + timezone.timedelta(days=1)
        )
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="pass12345"
        )
        self.reservation = Reservation.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            row=1,
            seat=1,
            performance=self.performance,
            reservation=self.reservation
        )

    def test_genre_str(self):
        self.assertEqual(str(self.genre), "Трагедія")

    def test_actor_full_name_property(self):
        self.assertEqual(self.actor.full_name, "Іван Франко")

    def test_play_str(self):
        self.assertEqual(str(self.play), "Гамлет")

    def test_theatre_hall_capacity(self):
        self.assertEqual(self.hall.capacity, 50)

    def test_performance_str(self):
        self.assertIn("Гамлет", str(self.performance))
        self.assertIn("at", str(self.performance))

    def test_reservation_str(self):
        self.assertIn("Reservation #", str(self.reservation))

    def test_ticket_str(self):
        self.assertIn("Ticket for", str(self.ticket))
        self.assertIn("Row 1", str(self.ticket))
