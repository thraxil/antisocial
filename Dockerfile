FROM thraxil/django.base:2022-06-11-1117f68671b75
COPY docker-run.sh /run.sh
COPY package.json /node/
RUN cd /node && npm install && touch /node/node_modules/sentinal
COPY requirements.txt /app/requirements.txt
RUN /ve/bin/pip3 install -r /app/requirements.txt && touch /ve/sentinal
WORKDIR /app
COPY . /app/
RUN VE=/ve/ MANAGE="/ve/bin/python3 manage.py" NODE_MODULES=/node/node_modules make all
EXPOSE 8000
ENV APP antisocial
ENTRYPOINT ["/run.sh"]
CMD ["run"]
