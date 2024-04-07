from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, ScheduleViewSet, BookingViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('schedules', ScheduleViewSet)
router.register('bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
