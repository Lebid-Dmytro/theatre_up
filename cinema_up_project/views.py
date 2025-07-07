from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Play, Performance, Reservation
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (
    PlaySerializer,
    PerformanceSerializer,
    ReservationSerializer,
)


@extend_schema(
    summary="Manage plays",
    description="Allows listing, creating, updating and deleting "
                "plays. Supports filtering by title and genre.",
    parameters=[
        OpenApiParameter(
            name="title",
            description="Filter by title",
            required=False,
            type=str
        ),
        OpenApiParameter(
            name="genre",
            description="Filter by genre ID",
            required=False,
            type=int
        ),
    ]
)
class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("genres", "actors")
    serializer_class = PlaySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        title = self.request.query_params.get("title")
        genre_id = self.request.query_params.get("genre")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)

        return queryset

    @extend_schema(
        summary="Upload image for a play",
        description="Upload an image for a specific play by ID.",
        methods=["POST"],
        request={"multipart/form-data": {
            "image": {"type": "string", "format": "binary"}}
        },
        responses={200: {
            "type": "object",
            "properties": {"message": {"type": "string"}}}
        },
    )
    @action(
        detail=True, methods=["post"],
        permission_classes=[IsAdminOrReadOnly],
        parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request, pk=None):
        play = self.get_object()
        image = request.FILES.get("image")

        if not image:
            return Response({"error": "No image uploaded."}, status=400)

        play.image = image
        play.save()

        return Response({
            "message": "Image uploaded successfully.",
            "image_url": request.build_absolute_uri(play.image.url)
        })


@extend_schema(
    summary="List performances",
    description="List performances with optional filtering by play "
                "title or genre. Supports sorting by show_time.",
    parameters=[
        OpenApiParameter(
            name="title",
            description="Filter by play title",
            required=False,
            type=str
        ),
        OpenApiParameter(
            name="genre",
            description="Filter by genre ID",
            required=False,
            type=int
        ),
        OpenApiParameter(
            name="sort_by",
            description="Sort by show_time (date or -date)",
            required=False,
            type=str
        ),
    ]
)
class PerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Performance.objects.select_related(
        "play", "theatre_hall").prefetch_related("play__genres")
    serializer_class = PerformanceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = self.queryset
        title = self.request.query_params.get("title")
        genre_id = self.request.query_params.get("genre")
        sort_by = self.request.query_params.get("sort_by")

        if title:
            queryset = queryset.filter(play__title__icontains=title)
        if genre_id:
            queryset = queryset.filter(play__genres=genre_id)
        if sort_by == "date":
            queryset = queryset.order_by("show_time")
        elif sort_by == "-date":
            queryset = queryset.order_by("-show_time")

        return queryset


@extend_schema(
    summary="Manage reservations",
    description="Authenticated users can view and "
                "create their own reservations only."
)
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.prefetch_related("tickets", "user")
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Reservation.objects.none()
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
