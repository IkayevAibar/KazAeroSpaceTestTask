from django.contrib import admin
from .models import CustomUser, Gym, Schedule, Booking

admin.site.register(CustomUser)
admin.site.register(Gym)
admin.site.register(Schedule)
admin.site.register(Booking)
