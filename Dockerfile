# ---- Base image ----
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (better layer caching)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app/ .

# App listens on port 5000
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
