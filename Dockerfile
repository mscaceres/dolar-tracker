FROM python:3.5

RUN mkdir -p /usr/src/app/wheelhouse
WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install wheel==0.29.0

COPY . /usr/src/app
RUN python setup.py test
RUN pip wheel --wheel-dir=/usr/src/app/wheelhouse .
RUN pip install --use-wheel --no-index --find-links=/usr/src/app/wheelhouse dollar-tracker
RUN rm -fr *
EXPOSE 8080

CMD bash