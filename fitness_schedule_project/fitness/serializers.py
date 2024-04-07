from rest_framework import serializers
from .models import CustomUser, Schedule, Booking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = '__all__'
        exclude = ("password", "is_superuser", "is_staff", "groups", "user_permissions")

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'full_name', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}, 'role': {'read_only': True}}

class UserTrainerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'full_name', 'gender', 'password', 'date_of_birth')
        extra_kwargs = {'password': {'write_only': True}}

class UserAdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'date_of_birth', 'gender')
        extra_kwargs = {'id': {'read_only': True}}

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ('trainer',)

class ScheduleAddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ('trainer',)

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
