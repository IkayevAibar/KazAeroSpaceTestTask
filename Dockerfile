FROM python:3.11.4

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY req.txt .
RUN pip install -r req.txt

COPY . .

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    apt-get clean

RUN python fitness_schedule_project/manage.py makemigrations
RUN python fitness_schedule_project/manage.py migrate

RUN python fitness_schedule_project/manage.py populate_db

CMD ["python", "fitness_schedule_project/manage.py", "runserver", "0.0.0.0:8000"]
