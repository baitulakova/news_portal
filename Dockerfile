FROM python:3

ENV DJANGO_SUPERUSER_PASSWORD admin
ENV DJANGO_SUPERUSER_EMAIL example@example.com
ENV DJANGO_SUPERUSER_USERNAME admin

COPY . .

RUN pip install django
RUN pip install psycopg2-binary
RUN pip install django-grappelli

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait

RUN chmod +x ./script.sh
RUN chmod +x ./wait

EXPOSE 8000

ENTRYPOINT /wait && ./script.sh