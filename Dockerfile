# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies

COPY . /app/

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# RUN cd /app/ticket_reservation
# RUN ls

# # Copy the project files
# COPY .ticket_reservation /app/

WORKDIR "/app/ticket_reservation/"
RUN python manage.py migrate

RUN python manage.py reset_berths

# RUN python manage.py reset_berths

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]