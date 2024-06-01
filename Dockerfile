FROM python:3.11.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY event_calendar/requirements.txt /code/
WORKDIR /code
RUN pip -V
RUN python --version
RUN pip install -r requirements.txt
COPY event_calendar/. /code/
