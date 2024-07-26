FROM python:3.12.1-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Remove migration files that match the pattern "000*"
EXPOSE 8002

# Run the application
CMD ["bash", "-c", "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8002"]
