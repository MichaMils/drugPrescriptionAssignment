# Use the official Python image as the base image
FROM python:3.9-alpine

RUN apk add --no-cache bash

# Set the working directory inside the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Define the command to run when the container starts
CMD ["python", "app.py"]
