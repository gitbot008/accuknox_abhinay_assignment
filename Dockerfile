FROM python:3.11.0


ENV PYTHONUNBUFFERED=1


RUN pip install --upgrade pip


COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt


COPY ./KAP_Backend /app


WORKDIR /app



COPY ./entrypoint.sh /


RUN chmod +x /entrypoint.sh


ENTRYPOINT ["/entrypoint.sh"]