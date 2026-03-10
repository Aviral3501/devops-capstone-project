# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY service service

# Create non-root user
RUN useradd --create-home theia

# Change ownership
RUN chown -R theia:theia /app

# Switch to non-root user
USER theia

# Expose application port
EXPOSE 8080

# Run application with gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:app"]