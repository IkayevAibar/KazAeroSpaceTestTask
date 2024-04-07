from django.utils import timezone

from .models import CustomUser, Gym, Schedule, Booking
from .serializers import UserSerializer, UserRegisterSerializer, UserAdditionalInfoSerializer, ScheduleSerializer, BookingSerializer

from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegisterSerializer
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
        
        user_data = {
            'email': email,
            'role': 'client',
            'password': password
        }
        serializer = UserRegisterSerializer(data=user_data)

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

        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Email and Password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_data = {
            'email': email,
            'role': 'client',
            'password': password
        }
        serializer = UserRegisterSerializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
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
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_class = [IsAuthenticated]
