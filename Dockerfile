# FROM nginx:mainline-alpine

# # --- Python Installation ---
# RUN apk add --no-cache python3 && \
#     python3 -m ensurepip && \
#     rm -r /usr/lib/python*/ensurepip && \
#     pip3 install --upgrade pip setuptools && \
#     if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
#     if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
#     rm -r /root/.cache

# # --- Work Directory ---
# WORKDIR /usr/src/app

# # --- Python Setup ---
# ADD . .
# RUN pip install -r app/requirements.txt

# # --- Nginx Setup ---
# COPY config/nginx/default.conf /etc/nginx/conf.d/
# RUN chmod g+rwx /var/cache/nginx /var/run /var/log/nginx
# RUN chgrp -R root /var/cache/nginx
# RUN sed -i.bak 's/^user/#user/' /etc/nginx/nginx.conf
# RUN addgroup nginx root

# # --- Expose and CMD ---
# EXPOSE 8080
# CMD gunicorn --bind 0.0.0.0:3001 app:app & nginx -g "daemon off;"






FROM python:3.7-slim-buster

WORKDIR /app

RUN apt-get update -y && apt-get install -y python3 python3-pip

COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD gunicorn --bind 0.0.0.0:8080 app:app
