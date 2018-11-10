FROM ubuntu:16.04
ADD . /app
VOLUME /app
RUN apt-get update
RUN apt-get install -y python3.5 python3-pip libmysqlclient-dev
RUN pip3 install -r /app/requirements.txt
RUN pip3 install gunicorn
WORKDIR /app
EXPOSE 8000
USER nobody
CMD /usr/local/bin/gunicorn -b 0.0.0.0 stackoverflow.wsgi:application
