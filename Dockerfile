FROM python:3.8.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /src 
WORKDIR /src/
COPY ./requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
COPY . /src/

EXPOSE 8000