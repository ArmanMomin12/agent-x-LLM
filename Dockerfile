# ===============================
#   AutoGPT Project - Dockerfile
#   Author: Arman Momin
#   Fresher Level Setup
# ===============================

# Use Python base image
FROM python:3.10-slim

# Set work directory inside container
WORKDIR /app

# Copy requirements first (for caching layers)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY . .

# Expose default port (change if needed)
EXPOSE 8000

# Run the app (adjust main file if needed)
CMD ["python", "main.py"]
