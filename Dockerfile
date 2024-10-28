# Dockerfile
FROM python:3.12.3-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Make the startup script executable
COPY startup.sh .
RUN chmod +x startup.sh

# Set environment variables
ENV FLASK_APP=library_management
ENV PORT=8080

# Use the startup script as the entrypoint
ENTRYPOINT ["./startup.sh"]