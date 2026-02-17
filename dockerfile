FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget gnupg libgconf-2-4 libatk1.0-0 libatk-bridge2.0-0 \
    libgdk-pixbuf2.0-0 libgtk-3-0 libgbm1 libnss3 libxss1 libasound2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps chromium

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "veritas_web_app:app"]
