from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', "admin")

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_ROLES = (
    ('client', 'Client'),
    ('trainer', 'Trainer'),
    ('admin', 'Admin'),
    )

    GENDER_OPTION = (
    ('male', 'Male'),
    ('female', 'Female'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(_('role'), max_length=20, choices=USER_ROLES, default="client")
    is_active = models.BooleanField(_('active'), default=True) # if client paid the subscription for fitness user'd be active, for our situation all users paid subscription :D
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    #additional information
    date_of_birth = models.DateField(null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_OPTION, null=False, blank=False, default="male")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

class Gym(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('Gym')
        verbose_name_plural = _('Gyms')


DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

class Schedule(models.Model):
    """
    Each trainer person can decide in which day he will work and and how much time. 
    
    Example: Trainer can choose day Monday as full work, and other days as half work day
    """
    
    trainer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20, choices=DAYS_OF_WEEK, default="Monday")
    start_time = models.TimeField()# a time when trainer will be available to help with gym activity
    end_time = models.TimeField()

    def __str__(self) -> str:
        return self.trainer.full_name + " - " + self.gym.name  + " - " + self.day_of_week  + " - " + self.start_time.__str__() + " - " + self.end_time.__str__()

    class Meta:
        verbose_name = _('Schedule')
        verbose_name_plural = _('Schedules')

class Booking(models.Model):
    """
    Every client person can pick a schedule with trainer, gym and also day of the week, time when trainer available included from schedule list
    and then should choose a time between that trainer leaved in schedule information.
    
    
    Example: Trainer made a schedule to train people on every Monday from 08:00 AM to 12:00 AM, so client can choose that schedule.
    """
    
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client_bookings')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    start_time = models.TimeField(null=True, blank=True) # a time when client will start gym activity
    end_time = models.TimeField(null=True, blank=True)

    def intersects_with_schedule(self, schedule):
        
        if self.schedule.day_of_week != schedule.day_of_week:
            return False

        if (self.schedule.start_time < schedule.end_time) and (self.schedule.end_time > schedule.start_time):
            return True
        

        return False
    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')

