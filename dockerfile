FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg libgconf-2-4 libatk1.0-0 libatk-bridge2.0-0 \
    libgdk-pixbuf2.0-0 libgtk-3-0 libgbm1 libnss3 libxss1 libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright browsers with explicit path
ENV PLAYWRIGHT_BROWSERS_PATH=/app/ms-playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy app files
COPY . .

# Expose port
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "veritas_web_app:app"]
