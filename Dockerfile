FROM python:3.13-alpine
RUN pip3 install --no-cache-dir 'requests==2.34.2' 'psycopg2-binary==2.9.13' && adduser -S -H app
WORKDIR /app
COPY fuelprices-collector.py .
USER app
CMD ["python3", "-u", "fuelprices-collector.py"]
