FROM thraxil/django.base:2017-07-24-908add65ae62a7fa6a482ad5033b9942c25e4022f587b97ab62e5d94ea7308f1
COPY package.json /node/
RUN cd /node && npm install && touch /node/node_modules/sentinal
COPY requirements.txt /app/requirements.txt
RUN /ve/bin/pip install -r /app/requirements.txt && touch /ve/sentinal
WORKDIR /app
COPY . /app/
RUN VE=/ve/ MANAGE="/ve/bin/python manage.py" NODE_MODULES=/node/node_modules make all
EXPOSE 8000
ADD docker-run.sh /run.sh
ENV APP antisocial
ENTRYPOINT ["/run.sh"]
CMD ["run"]
