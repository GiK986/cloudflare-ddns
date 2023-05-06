FROM python:alpine
LABEL authors="gik986"

# Environment variables
ENV CF_API_KEY=""
ENV CF_ZONE_ID=""
ENV CF_RECORD_NAME=""
ENV CF_TTL=1
ENV CF_PROXIED=False
ENV CF_CHECK_INTERVAL=60
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt

# copy project source file(s)
WORKDIR /app

COPY . .

CMD ["python", "-u", "/app/main.py"]
