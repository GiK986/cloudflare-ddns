FROM python:alpine
LABEL authors="gik986"

# Environment variables
ENV CF_API_TOKEN=""
ENV CF_ZONE_ID=""
ENV CF_RECORD_NAME=""
ENV CF_TTL=1
ENV CF_PROXY=false
ENV CF_CHECK_INTERVAL=60
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app/ .

CMD ["python", "-u", "main.py"]
