from datetime import time

from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend

from .models import CustomUser, Gym, Schedule, Booking
from .serializers import UserSerializer, UserRegisterSerializer, UserTrainerRegisterSerializer, UserAdditionalInfoSerializer, \
                    ScheduleSerializer, ScheduleCreateSerializer, ScheduleAddingSerializer, BookingSerializer

from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegisterSerializer
        if self.action == 'registerTrainer':
            return UserTrainerRegisterSerializer
        if self.action == 'update_additional_info':
            return UserAdditionalInfoSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['register']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
    
        return [permission() for permission in permission_classes]
    

    @action(detail=False, methods=['post'])
    def register(self, request, pk=None):
        """ Method for register a client"""

        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Email and Password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def registerTrainer(self, request, pk=None):
        """ Method for registering a trainer by admin"""
        
        if not request.user.role == "admin":
            return Response({'error': 'Only admins can register trainers'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.role = "trainer"
            user.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def update_additional_info(self, request, pk=None):
        """ Method for updating additional information of a client
        
        Usually person only by self should can change own information
        """

        serializer = self.get_serializer(instance=request.user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['trainer', 'gym', 'day_of_week', 'start_time', 'end_time']

    def get_serializer_class(self):
        if self.action == 'create_schedule':
            return ScheduleCreateSerializer
        if self.action == 'add_this_schedule':
            return ScheduleAddingSerializer
        return ScheduleSerializer

    @action(detail=False, methods=['post'])
    def create_schedule(self, request):
        serializer = self.get_serializer(data=request.data)

        if not request.user.role == "trainer":
            return Response({'error': 'Only trainers can create schedule'}, status=status.HTTP_403_FORBIDDEN)

        
        if serializer.is_valid():

            day_of_week = serializer.validated_data['day_of_week']
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            
            if time(0, 1) <= start_time <= time(5, 59) or time(0, 1) <= end_time <= time(5, 59):
                return Response({'error': 'The fitness center is closed between 00:00 and 06:00'},
                                status=status.HTTP_400_BAD_REQUEST)
        
            if self.schedule_intersects_for_same_day(self, request.user, day_of_week, start_time, end_time):
                return Response({'error': 'The schedule intersects with another schedule of the same trainer'},
                                 status=status.HTTP_400_BAD_REQUEST)
            

            serializer.save(trainer=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def get_own_schedule(self, request):
        queryset = self.get_queryset().filter(trainer=request.user)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_this_schedule(self, request, pk=None):
        
        if not request.user.role == "client":
            return Response({'error': 'Only clients can book a schedule'}, status=status.HTTP_403_FORBIDDEN)

        try:
            schedule = self.get_queryset().get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Schedule does not exist"}, status=status.HTTP_404_NOT_FOUND)

        client = request.user

        client_bookings = Booking.objects.filter(client=client)

        for booking in client_bookings:
            if booking.intersects_with_schedule(schedule):
                return Response({"error": "Selected schedule intersects with existing booking"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                booking = Booking.objects.create(client=client, schedule=schedule)
        except IntegrityError:
            return Response({"error": "Failed to create booking"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({
            "message":"added to client schedule", 
            "client_id":client.id, 
            "booking_id":booking.id,
            "booking_details": {
                "schedule_id": schedule.id,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "week_day": schedule.day_of_week,
                "trainer_full_name": schedule.trainer.full_name
                }
            }, status=status.HTTP_201_CREATED)

    
    @staticmethod
    def schedule_intersects_for_same_day(self, user, day_of_week, start_time, end_time) -> bool:
        intersecting_schedules = Schedule.objects.filter(
            trainer=user,
            day_of_week=day_of_week,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        return intersecting_schedules.exists()
    
    

class BookingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_class = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'schedule', 'start_time', 'end_time', 'schedule__day_of_week', 'schedule__start_time', 'schedule__end_time']
    
    @action(detail=False, methods=['get'])
    def get_own_schedule(self, request):
        if not request.user.role == "client":
            return Response({'error': 'Only clients have permissions to watch own booking'}, status=status.HTTP_403_FORBIDDEN)
        
        queryset = self.get_queryset().filter(client=request.user)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
