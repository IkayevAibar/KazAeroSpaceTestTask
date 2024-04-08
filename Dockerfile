FROM python:3.11.4

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY req.txt .
RUN pip install -r req.txt

COPY . .

CMD ["python", "fitness_schedule_project/manage.py", "runserver", "0.0.0.0:8000"]
