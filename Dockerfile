FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /usr/src/requirements.txt

WORKDIR /usr/src

RUN pip3 install -r requirements.txt

COPY . /usr/src

CMD [ "flask", "app.py" ]