FROM python:3.9.2-alpine
RUN pip3 install --upgrade pip
RUN pip3 install 'requests==2.31.0' 'psycopg2-binary==2.9.6'
WORKDIR /collector
COPY fuelprices-collector.py .
COPY fuelprices-collector-crontab .
COPY entrypoint.sh .
RUN chmod +x /collector/entrypoint.sh && cat /collector/fuelprices-collector-crontab >> /etc/crontabs/root
CMD ["/collector/entrypoint.sh"]
