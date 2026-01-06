# Use a more recent official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Update package lists
RUN apt-get update

# Install necessary PostgreSQL client
RUN apt-get install -y postgresql-client

# Install psycopg2-binary
RUN pip install psycopg2-binary

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
