FROM thraxil/django.base:2017-02-18-a75c79f20e8bdc6c9b624e9159296209aa15fe6a
COPY package.json /node/
RUN cd /node && npm install && touch /node/node_modules/sentinal
COPY requirements.txt /app/requirements.txt
RUN /ve/bin/pip install -r /app/requirements.txt && touch /ve/sentinal
WORKDIR /app
COPY . /app/
RUN VE=/ve/ MANAGE="/ve/bin/python manage.py" NODE_MODULES=/node/node_modules make all
RUN cp -a /node/node_modules /app && make webpack
EXPOSE 8000
ADD docker-run.sh /run.sh
ENV APP antisocial
ENTRYPOINT ["/run.sh"]
CMD ["run"]
