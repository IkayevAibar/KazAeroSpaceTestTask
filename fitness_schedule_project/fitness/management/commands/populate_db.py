import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from ...models import Gym, Schedule, Booking

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Create sample gyms
        gyms = ['Gym A', 'Gym B', 'Gym C']
        for gym_name in gyms:
            Gym.objects.create(name=gym_name)

        # Create sample users
        clients = []
        trainers = []
        for i in range(5):
            client = User.objects.create_user(email=f'client{i+1}@example.com', password='password', full_name=f'Client {i+1}')
            trainer = User.objects.create_user(email=f'trainer{i+1}@example.com', password='password', full_name=f'Trainer {i+1}', role='trainer')
            clients.append(client)
            trainers.append(trainer)

        # Create sample schedules
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for trainer in trainers:
            for day in days_of_week:
                start_time = timezone.now().replace(hour=random.randint(8, 12), minute=0, second=0, microsecond=0)
                end_time = (start_time + timezone.timedelta(hours=4)).replace(microsecond=0)
                Schedule.objects.create(trainer=trainer, gym=Gym.objects.first(), day_of_week=day, start_time=start_time.time(), end_time=end_time.time())

        # Create sample bookings
        for client in clients:
            for _ in range(3):
                schedule = Schedule.objects.order_by('?').first()
                start_time = schedule.start_time
                end_time = schedule.end_time
                Booking.objects.create(client=client, schedule=schedule, start_time=start_time, end_time=end_time)

        self.stdout.write(self.style.SUCCESS('Sample data has been successfully populated'))
