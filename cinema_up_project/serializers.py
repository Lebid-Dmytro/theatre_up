from rest_framework import serializers
from .models import Play, Performance, Reservation, Ticket


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ["id", "title", "description", "genres", "actors", "image"]


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance"]


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user", "tickets"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        reservation = Reservation.objects.create(**validated_data)
        for tk in tickets_data:
            Ticket.objects.create(reservation=reservation, **tk)
        return reservation
