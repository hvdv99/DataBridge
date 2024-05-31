FROM python:3.11-slim
LABEL authors="huubvandevoort"

ENV PYTHONUNBUFFERED=1

# Define build-time variables
ARG APP_HOME=/usr/src/app

# Create application directory
RUN mkdir -p $APP_HOME

# Set the working directory
WORKDIR $APP_HOME

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the current directory contents into the container
COPY services ./services
COPY data ./data

WORKDIR $APP_HOME/services

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "ui.app:app"]