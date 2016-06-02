FROM python:3.5

RUN mkdir -p /usr/src/app/wheelhouse && mkdir -p /usr/src/app/dollar-tracker
WORKDIR /usr/src/app/dollar-tracker

RUN pip install --upgrade pip
RUN pip install wheel==0.29.0 && pip install pytest

COPY . /usr/src/app/dollar-tracker
RUN pip wheel --wheel-dir=/usr/src/app/wheelhouse .
RUN pip install --use-wheel --no-index --find-links=/usr/src/app/wheelhouse dollar-tracker
RUN rm -fr /usr/src/app/dollar-tracker/dollar_tracker /usr/src/app/dollar-tracker/*.py /usr/src/app/dollar-tracker/Dockerfile
VOLUME /usr/src/app/dollar-tracker

ENTRYPOINT ["dollar-tracker"]
CMD ["track"]