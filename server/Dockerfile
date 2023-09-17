FROM ubuntu

RUN apt-get update -yqq
RUN apt-get install -yqq nginx-full python3 git duplicity
RUN mkdir -p /www
WORKDIR /www

COPY nginx.conf /etc/nginx/nginx.conf
COPY site.conf /etc/nginx/sites-enabled/default

COPY init_nginx.bash "/init_nginx.bash"
ENTRYPOINT [ "/init_nginx.bash" ]
