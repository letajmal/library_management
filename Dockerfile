# Dockerfile
FROM python:3.12.3-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set environment variable for Flask app
ENV FLASK_APP=library_management

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]