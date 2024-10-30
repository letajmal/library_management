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

# Set environment variables
ENV FLASK_APP=library_management
ENV PORT=8080

CMD ["flask", "run", "--host=0.0.0.0", "--port=$PORT"]